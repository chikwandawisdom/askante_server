from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes, APIView
from rest_framework.permissions import IsAuthenticated

from employees.models.employees import Employee
from fundamentals.custom_responses import success_w_data, err_w_msg, success_w_msg
from institutions.methods.academic_year import get_active_academic_year
from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer
from institutions.models.timetables import Period, PeriodReadSerializer
from registry.models.attendance_group import AttendanceGroup
from students.models.students import Student
from users.permissions import IsTeacher, IsStudent, IsSuperUser
from .models.assignments import (
    Assignment,
    AssignmentWriteSerializer,
    AssignmentReadSerializer,
)
from .models.exams import Exam, ExamWriteSerializer, ExamReadSerializer
from .models.lesson import Lesson, Attendance, AttendanceReadSerializer
from .models.marking_criteria import (
    MarkingCriterion,
    MarkingCriterionWriteSerializer,
    MarkingCriterionReadSerializer,
)
from .models.marks import (
    Mark,
    MarksWriteSerializer,
    MarksReadSerializer,
    filter_marks_by_student,
    filter_marks_by_assessment_id,
)
from .models.settings import Settings, SettingsSerializer
from .models.term_results import (
    TermResult,
    TermResultWriteSerializer,
    TermResultReadSerializer,
)
from .queries import (
    filter_by_class_subject,
    filter_by_period_day,
    filter_by_academic_year,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_teachers_class_list(request):
    employee = Employee.objects.get(user=request.user)

    class_subjects = ClassSubject.objects.filter(teacher=employee).order_by("-id")
    class_subjects = ClassSubjectReadSerializer(class_subjects, many=True).data

    return success_w_data(data=class_subjects, msg="Class list fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_teachers_periods(request):
    params = request.query_params

    periods = Period.objects.filter(
        Q(class_subject__teacher__user=request.user)
        & filter_by_class_subject(params.get("class_subject"))
        & filter_by_period_day(params.get("day"))
    ).order_by("day", "period")
    periods = PeriodReadSerializer(periods, many=True).data

    return success_w_data(data=periods, msg="Periods fetched successfully")


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsTeacher])
def submit_attendance(request):
    data = request.data.copy()
    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    try:
        lesson = Lesson.objects.filter(period=data["period"], date=data["date"]).first()
        if lesson is None:
            lesson = Lesson.objects.create(
                period_id=data["period"],
                date=data["date"],
                academic_year=active_academic_year,
            )

        attendance = Attendance.objects.filter(
            lesson=lesson, student_id=data["student"]
        ).first()

        if attendance:
            attendance.delete()

        attendance_group = AttendanceGroup.objects.get(id=data["attendance_group"])
        Attendance.objects.create(
            lesson=lesson,
            student_id=data["student"],
            attendance_group=attendance_group,
            academic_year=active_academic_year,
        )

        return success_w_msg(msg="Attendance submitted successfully")
    except Exception as e:
        return err_w_msg(msg=str(e))


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_attendance_list(request):
    params = request.query_params

    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    lesson = Lesson.objects.filter(
        Q(period=params.get("period"))
        & Q(date=params.get("date"))
        & filter_by_academic_year(academic_year=active_academic_year)
    ).first()
    if lesson is None:
        return success_w_data(data=[], msg="No attendance found")

    attendance = Attendance.objects.select_related(
        "student", "attendance_group"
    ).filter(lesson=lesson)
    attendance = AttendanceReadSerializer(attendance, many=True).data
    return success_w_data(data=attendance, msg="Attendance fetched successfully")


class MarkingCriterionList(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def post(request):
        data = request.data.copy()
        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)
        data["academic_year"] = active_academic_year.id

        serializer = MarkingCriterionWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Marking criterion added successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)

        marking_criteria = MarkingCriterion.objects.filter(
            Q(class_subject=params.get("class_subject"))
            & filter_by_academic_year(active_academic_year)
        ).order_by("-id")

        marking_criteria = MarkingCriterionReadSerializer(
            marking_criteria, many=True
        ).data

        return success_w_data(
            data=marking_criteria, msg="Marking criteria fetched successfully"
        )


class MarkingCriterionDetail(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def get(request, pk):
        marking_criterion = MarkingCriterion.objects.get(id=pk)
        marking_criterion = MarkingCriterionReadSerializer(marking_criterion).data
        return success_w_data(
            data=marking_criterion, msg="Marking criterion fetched successfully"
        )

    @staticmethod
    def patch(request, pk):
        marking_criterion = MarkingCriterion.objects.get(id=pk)
        serializer = MarkingCriterionWriteSerializer(
            instance=marking_criterion, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Marking criterion updated successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def delete(request, pk):
        marking_criterion = MarkingCriterion.objects.get(id=pk)
        marking_criterion.delete()
        return success_w_msg(msg="Marking criterion deleted successfully")


class AssignmentList(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def post(request):
        data = request.data.copy()
        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)
        data["academic_year"] = active_academic_year.id

        # checking if due_date is in the past. parse the due_date first which is a YYYY-MM-DDTHH:MM:SS.sssZ string
        due_date = datetime.strptime(data["due_date"], "%Y-%m-%dT%H:%M:%S.%fZ")
        if due_date < datetime.now():
            return err_w_msg(msg="Due date cannot be in the past")

        serializer = AssignmentWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Assignment added successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)

        assignments = Assignment.objects.filter(
            Q(class_subject=params.get("class_subject"))
            & filter_by_academic_year(active_academic_year)
        ).order_by("-id")

        assignments = AssignmentReadSerializer(assignments, many=True).data

        return success_w_data(data=assignments, msg="Assignments fetched successfully")


class AssignmentDetail(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def get(request, pk):
        assignment = Assignment.objects.get(id=pk)
        assignment = AssignmentReadSerializer(assignment).data
        return success_w_data(data=assignment, msg="Assignment fetched successfully")

    @staticmethod
    def patch(request, pk):
        assignment = Assignment.objects.get(id=pk)
        serializer = AssignmentWriteSerializer(
            instance=assignment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Assignment updated successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def delete(request, pk):
        assignment = Assignment.objects.get(id=pk)
        assignment.delete()
        return success_w_msg(msg="Assignment deleted successfully")


class ExamList(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def post(request):
        data = request.data.copy()
        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)
        data["academic_year"] = active_academic_year.id

        serializer = ExamWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Exam added successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)

        exams = Exam.objects.filter(
            Q(class_subject=params.get("class_subject"))
            & filter_by_academic_year(active_academic_year)
        ).order_by("-id")

        exams = ExamReadSerializer(exams, many=True).data

        return success_w_data(data=exams, msg="Exams fetched successfully")


class ExamDetail(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def get(request, pk):
        exam = Exam.objects.get(id=pk)
        exam = ExamReadSerializer(exam).data
        return success_w_data(data=exam, msg="Exam fetched successfully")

    @staticmethod
    def patch(request, pk):
        exam = Exam.objects.get(id=pk)
        serializer = ExamWriteSerializer(instance=exam, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Exam updated successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def delete(request, pk):
        exam = Exam.objects.get(id=pk)
        exam.delete()
        return success_w_msg(msg="Exam deleted successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_teachers_monthly_calendar(request):
    params = request.query_params

    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    current_month_start_date = datetime.strptime(
        params.get("date"), "%Y-%m-%d"
    ).replace(day=1)
    current_month_end_date = current_month_start_date.replace(
        day=1, month=current_month_start_date.month + 1
    ) - timedelta(days=1)

    # loop through the days of the month
    monthly_calendar = []
    current_date = current_month_start_date
    while current_date <= current_month_end_date:
        day = {
            "date": current_date.strftime("%Y-%m-%d"),
            "day": current_date.strftime("%A"),
        }

        events = []

        # periods
        periods = (
            Period.objects.select_related(
                "class_subject___class", "class_subject__subject"
            )
            .filter(
                Q(class_subject__teacher__user=request.user)
                & filter_by_period_day(current_date.strftime("%A"))
            )
            .order_by("period")
        )
        for period in periods:
            events.append(
                {
                    "type": "period",
                    "id": period.id,
                    "title": f"{period.class_subject._class.name} - ({period.start} - {period.end})",
                    "subject": period.class_subject.subject.name,
                }
            )

        # assignments
        assignments = Assignment.objects.filter(
            Q(class_subject__teacher__user=request.user)
            & Q(due_date__date=current_date)
            & filter_by_academic_year(active_academic_year)
        ).order_by("due_date")

        for assignment in assignments:
            last_time = assignment.due_date.time()
            first_time = (datetime.combine(datetime.min, last_time) - timedelta(minutes=60)).time()
            events.append(
                {
                    "type": "assignment",
                    "id": assignment.id,
                    "title": f"{assignment.title} - ({first_time} - {last_time})",
                    "subject": assignment.class_subject.subject.name,
                }
            )

        # exams
        exams = Exam.objects.filter(
            Q(class_subject__teacher__user=request.user)
            & Q(
                date__day=current_date.day,
                date__month=current_date.month,
                date__year=current_date.year,
            )
            & filter_by_academic_year(active_academic_year)
        ).order_by("date")

        for exam in exams:
            events.append(
                {
                    "type": "exam",
                    "id": exam.id,
                    "title": f'{exam.title} - ({exam.start} - {exam.end})',
                    "subject": exam.class_subject.subject.name,
                }
            )

        day["events"] = events
        monthly_calendar.append(day)

        current_date += timedelta(days=1)

    return success_w_data(
        data=monthly_calendar, msg="Monthly calendar fetched successfully"
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_marking_options_for_a_class(request):
    params = request.query_params
    marking_options = []

    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    exams = Exam.objects.filter(class_subject=params.get("class_subject")).order_by(
        "id"
    )
    assignments = Assignment.objects.filter(
        Q(class_subject=params.get("class_subject"))
        & filter_by_academic_year(active_academic_year)
    ).order_by("id")

    for assignment in assignments:
        marking_options.append(
            {
                "assessment_type": "assignment",
                "id": assignment.id,
                "title": assignment.title,
                "max_marks": assignment.max_marks,
                "marking_criterion": assignment.marking_criterion.id,
            }
        )

    for exam in exams:
        marking_options.append(
            {
                "assessment_type": "exam",
                "id": exam.id,
                "title": exam.title,
                "max_marks": exam.max_marks,
                "marking_criterion": exam.marking_criterion.id,
            }
        )

    return success_w_data(
        data=marking_options, msg="Marking options fetched successfully"
    )


class MarkList(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def post(request):
        data = request.data.copy()
        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)
        data["academic_year"] = active_academic_year.id

        serializer = MarksWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Mark added successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params

        employee = Employee.objects.get(user=request.user)
        active_academic_year = get_active_academic_year(employee.institution)

        marks = Mark.objects.filter(
            Q(class_subject=params.get("class_subject"))
            & filter_marks_by_student(params.get("student"))
            & filter_marks_by_assessment_id(params.get("assessment_id"))
            & filter_by_academic_year(active_academic_year)
        ).order_by("-id")

        marks = MarksReadSerializer(marks, many=True).data

        return success_w_data(data=marks, msg="Marks fetched successfully")


class MarkDetail(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    @staticmethod
    def get(request, pk):
        mark = Mark.objects.get(id=pk)
        mark = MarksReadSerializer(mark).data
        return success_w_data(data=mark, msg="Mark fetched successfully")

    @staticmethod
    def patch(request, pk):
        mark = Mark.objects.get(id=pk)
        serializer = MarksWriteSerializer(
            instance=mark, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Mark updated successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def delete(request, pk):
        mark = Mark.objects.get(id=pk)
        mark.delete()
        return success_w_msg(msg="Mark deleted successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_students_monthly_calendar(request):
    params = request.query_params
    student = Student.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(student.institution)

    current_month_start_date = datetime.strptime(
        params.get("date"), "%Y-%m-%d"
    ).replace(day=1)
    current_month_end_date = current_month_start_date.replace(
        day=1, month=current_month_start_date.month + 1
    ) - timedelta(days=1)

    # loop through the days of the month
    monthly_calendar = []
    current_date = current_month_start_date
    while current_date <= current_month_end_date:
        day = {
            "date": current_date.strftime("%Y-%m-%d"),
            "day": current_date.strftime("%A"),
            "periods": [],
            "assignments_due": [],
            "exams": [],
        }

        # periods
        periods = (
            Period.objects.select_related(
                "class_subject___class", "class_subject__subject"
            )
            .filter(
                Q(class_subject___class__students=student)
                & filter_by_period_day(current_date.strftime("%A"))
            )
            .order_by("period")
        )
        for period in periods:
            day["periods"].append(
                {
                    "id": period.id,
                    "title": f"{period.class_subject._class.name} - ({period.start} - {period.end})",
                    "subject": period.class_subject.subject.name,
                }
            )

        # assignments
        assignments = Assignment.objects.filter(
            Q(class_subject___class__students=student)
            & Q(due_date__date=current_date)
            & filter_by_academic_year(active_academic_year)
        ).order_by("due_date")

        for assignment in assignments:
            last_time = assignment.due_date.time()
            first_time = (datetime.combine(datetime.min, last_time) - timedelta(minutes=60)).time()
            day["assignments_due"].append(
                {
                    "id": assignment.id,
                    "title": f"{assignment.title} - ({first_time} - {last_time})",
                    "subject": assignment.class_subject.subject.name,
                }
            )

        # exams
        exams = Exam.objects.filter(
            Q(class_subject___class__students=student)
            & Q(
                date__day=current_date.day,
                date__month=current_date.month,
                date__year=current_date.year,
            )
            & filter_by_academic_year(active_academic_year)
        ).order_by("date")

        for exam in exams:
            day["exams"].append(
                {
                    "id": exam.id,
                    "title": f'{exam.title} - ({exam.start} - {exam.end})',
                    "subject": exam.class_subject.subject.name,
                }
            )

        monthly_calendar.append(day)

        current_date += timedelta(days=1)

    return success_w_data(
        data=monthly_calendar, msg="Monthly calendar fetched successfully"
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_attendance_list_for_student(request):
    params = request.query_params
    student = Student.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(student.institution)

    attendance = Attendance.objects.select_related(
        "student", "attendance_group"
    ).filter(
        Q(student=student)
        & Q(lesson__period__class_subject=params.get("class_subject"))
    )
    attendance = AttendanceReadSerializer(attendance, many=True).data
    return success_w_data(data=attendance, msg="Attendance fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_assignments_for_student(request):
    params = request.query_params
    student = Student.objects.get(user=request.user)

    active_academic_year = get_active_academic_year(student.institution)

    assignments = Assignment.objects.filter(
        Q(class_subject=params.get("class_subject"))
        & Q(class_subject___class__students=student)
        & filter_by_academic_year(active_academic_year)
    ).order_by("-id")

    assignments = AssignmentReadSerializer(assignments, many=True).data

    return success_w_data(data=assignments, msg="Assignments fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_exams_for_students(request):
    params = request.query_params
    student = Student.objects.get(user=request.user)

    exams = Exam.objects.filter(
        Q(class_subject=params.get("class_subject"))
        & Q(class_subject___class__students=student)
        & filter_by_academic_year(get_active_academic_year(student.institution))
    ).order_by("-id")

    exams = ExamReadSerializer(exams, many=True).data

    return success_w_data(data=exams, msg="Exams fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_class_subject_list_for_students(request):
    student = Student.objects.get(user=request.user)

    class_subjects = ClassSubject.objects.filter(Q(_class__students=student)).order_by(
        "-id"
    )

    class_subjects = ClassSubjectReadSerializer(class_subjects, many=True).data

    return success_w_data(
        data=class_subjects, msg="Class subjects fetched successfully"
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_periods_for_students(request):
    student = Student.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(student.institution)

    periods = Period.objects.filter(
        Q(class_subject___class__students=student)
        & filter_by_academic_year(active_academic_year)
    ).order_by("day", "period")

    periods = PeriodReadSerializer(periods, many=True).data

    return success_w_data(data=periods, msg="Periods fetched successfully")


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsTeacher])
def submit_term_result(request):
    data = request.data.copy()
    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)
    data["academic_year"] = active_academic_year.id

    # duplicate check
    term_result = TermResult.objects.filter(
        Q(term=data["term"])
        & Q(student=data["student"])
        & Q(class_subject=data["class_subject"])
        & Q(academic_year=active_academic_year)
    ).first()

    if term_result:
        serializer = TermResultWriteSerializer(term_result, data=data, partial=True)
      
        if serializer.is_valid():
            print(serializer.is_valid())
            serializer.save()
            return success_w_msg(msg="Term result submitted successfully")
        
        # print(serializer.errors)
        return err_w_msg(msg="Term result already submitted for this student")
    
    

    serializer = TermResultWriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return success_w_msg(msg="Term result submitted successfully")
    return err_w_msg(msg=serializer.errors)


def filter_term_results_by_student(student):
    if student is None:
        return Q()
    return Q(student=student)


def filter_term_results_by_term(term):
    if term is None:
        return Q()
    return Q(term=term)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_term_result(request):
    params = request.query_params

    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    term_results = TermResult.objects.filter(
        Q(class_subject=params.get("class_subject"))
        & Q(academic_year=active_academic_year)
        & filter_term_results_by_student(params.get("student"))
        & filter_term_results_by_term(params.get("term"))
    ).order_by("-id")

    term_results = TermResultReadSerializer(term_results, many=True).data

    return success_w_data(data=term_results, msg="Term results fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_settings(request):
    if request.user.role != "admin" and not request.user.is_superuser:
        return err_w_msg(msg="You are not authorized to view settings")
    settings = Settings.objects.first()
    settings = SettingsSerializer(settings).data
    return success_w_data(data=settings, msg="Settings fetched successfully")


@api_view(["PATCH"])
@permission_classes([IsAuthenticated, IsSuperUser])
def update_settings(request):
    settings = Settings.objects.first()
    serializer = SettingsSerializer(instance=settings, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_w_msg(msg="Settings updated successfully")
    return err_w_msg(msg=serializer.errors)


# get students marks
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_student_marks(request):
    student = Student.objects.get(user=request.user)
    subject = request.query_params.get('subject')

    filters = Q(student=student)
    if subject:
        filters &= Q(class_subject__subject=subject)

    marks = Mark.objects.filter(filters)
    marks = MarksReadSerializer(marks, many=True).data
    return success_w_data(data=marks, msg="Marks fetched successfully")


# get students term results
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsStudent])
def get_student_term_results(request):
    student = Student.objects.get(user=request.user)
    term_results = TermResult.objects.filter(student=student)
    term_results = TermResultReadSerializer(term_results, many=True).data
    return success_w_data(data=term_results, msg="Term results fetched successfully")
