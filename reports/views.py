from django.db.models import Sum, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from django.utils import timezone

from academic.models.assignments import Assignment
from academic.models.exams import Exam
from academic.models.lesson import Attendance, AttendanceReadSerializer
from academic.models.term_results import TermResult, TermResultReadSerializer
from academic.queries import filter_by_academic_year, filter_by_period_day
from book_shop.models.book_purchase import BookPurchase
from employees.models.employees import Employee, EmployeeReadSerializer
from finance.models.payments import Payment
from fundamentals.custom_responses import success_w_data, err_forbidden, err_w_msg
from institutions.methods.academic_year import get_active_academic_year
from institutions.models.class_subjects import ClassSubject
from institutions.models.classes import Class
from institutions.models.institution import Institution
from institutions.models.room import Room
from institutions.models.subjects import Subject
from institutions.models.timetables import Period
from students.models.students import Student, StudentReadSerializer
from users.permissions import IsTeacher


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_institution_overview(request):
    params = request.query_params

    institution = Institution.objects.filter(id=params.get('institution')).first()

    if institution is None:
        return err_w_msg('Institution not found')

    if institution.organization != request.user.organization:
        return err_forbidden()

    number_of_employees = Employee.objects.filter(
        institution=params.get('institution')
    ).count()

    number_of_male_employees = Employee.objects.filter(
        institution=params.get('institution'),
        gender='male'
    ).count()

    number_of_female_employees = Employee.objects.filter(
        institution=params.get('institution'),
        gender='female'
    ).count()

    number_of_students = Student.objects.filter(
        institution=params.get('institution')
    ).count()

    number_of_male_students = Student.objects.filter(
        institution=params.get('institution'),
        gender='male'
    ).count()

    number_of_female_students = Student.objects.filter(
        institution=params.get('institution'),
        gender='female'
    ).count()

    # FIX: SHOFIQUL, Subject has no foreign key name institution
    # number_of_subjects = Subject.objects.filter(
    #     institution=params.get('institution')
    # ).count()

    number_of_classes = Class.objects.filter(
        institution=params.get('institution')
    ).count()

    number_of_rooms = Room.objects.filter(
        institution=params.get('institution')
    ).count()

    current_academic_year = get_active_academic_year(institution)
    if current_academic_year is None:
        current_academic_year = 'Academic year not set'
    # current_academic_year should be string of current_academic_year.start_date and current_academic_year.end_date
    current_academic_year = f'{current_academic_year.start_date} - {current_academic_year.end_date}'

    return success_w_data(data={
        'number_of_employees': number_of_employees,
        'number_of_male_employees': number_of_male_employees,
        'number_of_female_employees': number_of_female_employees,
        'number_of_students': number_of_students,
        'number_of_male_students': number_of_male_students,
        'number_of_female_students': number_of_female_students,
        # 'number_of_subjects': number_of_subjects, // TODO: fix by shamimferdous
        'number_of_classes': number_of_classes,
        'number_of_rooms': number_of_rooms,
        'current_academic_year': current_academic_year
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_7_days_attendance(request):
    params = request.query_params

    institution = Institution.objects.filter(id=params.get('institution')).first()

    if institution is None:
        return err_w_msg('Institution not found')

    if institution.organization != request.user.organization:
        return err_forbidden()

    number_of_students = Student.objects.filter(
        institution=params.get('institution')
    ).count()

    start_date = params.get('start_date')

    # parse start_date str (YYYY-MM-DD) to datetime object
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    results = []

    # loop through the last 7 days
    for i in range(7):
        date = start_date - timedelta(days=i)
        attendance = Attendance.objects.filter(
            student__institution=params.get('institution'),
            lesson__date=date,
            attendance_group__record_late_time=False
        ).count()

        percentage = (attendance / number_of_students) * 100
        results.append({
            'date': date,
            'percentage': percentage,
            'count': attendance
        })

    return success_w_data(data=results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_last_15_days_finance_data(request):
    params = request.query_params

    institution = Institution.objects.filter(id=params.get('institution')).first()

    if institution is None:
        return err_w_msg('Institution not found')

    if institution.organization != request.user.organization:
        return err_forbidden()

    start_date = params.get('start_date')

    # parse start_date str (YYYY-MM-DD) to datetime object
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    results = []

    # loop through the last 15 days
    for i in range(15):
        number_of_invoice = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i)
        ).count()

        number_of_paid_invoice = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i),
            status='paid'
        ).count()

        number_of_due_invoice = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i),
            status='due'
        ).count()

        total_amount = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i),
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_paid_amount = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i),
            status='paid'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        total_due_amount = Payment.objects.filter(
            institution=params.get('institution'),
            date=start_date - timedelta(days=i),
            status='due'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        results.append({
            'date': start_date - timedelta(days=i),
            'number_of_invoice': number_of_invoice,
            'number_of_paid_invoice': number_of_paid_invoice,
            'number_of_due_invoice': number_of_due_invoice,
            'total_amount': total_amount,
            'total_paid_amount': total_paid_amount,
            'total_due_amount': total_due_amount
        })

    return success_w_data(data=results)


#  >>>>>>>>>>>> Teachers Reports <<<<<<<<<<<<<<

# get teachers overview
@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teachers_overview(request):
    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    number_of_classes = ClassSubject.objects.filter(teacher=employee).order_by('-id').count()

    number_of_periods = Period.objects.filter(
        Q(class_subject__teacher__user=request.user)
    ).order_by('period').count()

    number_of_exams_taken = Exam.objects.filter(
        Q(class_subject__teacher__user=request.user) &
        filter_by_academic_year(active_academic_year)
    ).order_by('-id').count()

    number_of_assignments_taken = Assignment.objects.filter(
         Q(class_subject__teacher__user=request.user) &
        filter_by_academic_year(active_academic_year)
    ).order_by('-id').count()

    classes = ClassSubject.objects.filter(teacher=employee).values_list('_class_id', flat=True)
    total_students = Student.objects.filter(
        classes__id__in=classes,
        academic_year=active_academic_year
    ).distinct().count()

    return success_w_data(data={
        'number_of_classes': number_of_classes,
        'number_of_periods': number_of_periods,
        'number_of_exams_taken': number_of_exams_taken,
        'number_of_assignments_taken': number_of_assignments_taken,
        'total_students': total_students
    })

# get teachers class attendance
@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teachers_class_attendance(request):
    params = request.query_params

    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    periods = Period.objects.select_related('class_subject___class', 'class_subject__subject').filter(
        Q(class_subject__teacher__user=request.user)
        & filter_by_period_day(params.get('date'))
    ).order_by('period')

    attendance = Attendance.objects.filter(
        lesson__period__in=periods,
        academic_year=active_academic_year
    ).values('attendance_group__name').distinct()

    results = []

    for a in attendance:
        results.append({
            'name': a['attendance_group__name'],
            'count': Attendance.objects.filter(
                lesson__period__in=periods,
                academic_year=active_academic_year,
                attendance_group__name=a['attendance_group__name']
            ).count()
        })

    return success_w_data(data=results)

# total students by classes taught by the teacher
@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_students(request):
    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    classes = ClassSubject.objects.filter(teacher=employee).values('_class_id', '_class__name')

    if not classes:
        return success_w_data(data=[])

    class_student_counts = []
    for class_info in classes:
        class_id = class_info['_class_id']
        class_name = class_info['_class__name']
        student_count = Student.objects.filter(
            classes__id=class_id,
            academic_year=active_academic_year
        ).distinct().count()
        class_student_counts.append({
            'class_id': class_id,
            'class_name': class_name,
            'student_count': student_count
        })

    return success_w_data(data=class_student_counts)

# get teachers students list
@api_view(['GET'])
@permission_classes([IsTeacher])
def get_teacher_students_list(request):
    employee = Employee.objects.get(user=request.user)
    active_academic_year = get_active_academic_year(employee.institution)

    # Fetch the classes taught by the teacher
    classes = ClassSubject.objects.filter(teacher=employee).values_list('_class_id', flat=True)

    # Get filter parameters from the request
    class_id = request.query_params.get('class_id')
    gender = request.query_params.get('gender')
    subject_id = request.query_params.get('subject_id')

    # Fetch the students associated with these classes
    students = Student.objects.filter(
        classes__id__in=classes,
        academic_year=active_academic_year
    ).distinct()

    # Apply filters
    if class_id:
        students = students.filter(classes__id=class_id)
    if gender:
        students = students.filter(gender=gender)
    if subject_id:
        # Fetch the classes associated with the subject_id
        class_subjects = ClassSubject.objects.filter(subject_id=subject_id).values_list('_class_id', flat=True)
        students = students.filter(classes__id__in=class_subjects)

    # Prepare the list of students
    student_list = []
    for student in students:
        student_list.append({
            'id': student.student_id,
            'name': f'{student.first_name} {student.last_name}',
            'email': student.email,
            '_class': student.classes.filter(id__in=classes).first().name  # Assuming a student can be in multiple classes
        })

    return success_w_data(data=student_list)



# >>>>>>>>>>>> Final Reports <<<<<<<<<<<<<<

def filter_by_organization(organization):
    if organization is None:
        return Q()
    return Q(institution__organization=organization)


def filter_by_institution(institution):
    if institution is None:
        return Q()
    return Q(institution=institution)


def filter_students_by_grade_level(level):
    if level is None:
        return Q()
    return Q(grade__level=level)


def filter_students_by_class(_class):
    if _class is None:
        return Q()
    return Q(classes=_class)


def filter_students_by_subject(subject):
    if subject is None:
        return Q()
    return Q(classes__class_subjects__subject=subject)


def filter_by_gender(gender):
    if gender is None:
        return Q()
    return Q(gender=gender)


def filter_students_by_student_type(student_type):
    if student_type is None:
        return Q()
    return Q(student_type=student_type)


def filter_students_by_payments(term, status):
    if term is None:
        return Q()
    status = status or 'paid'
    return Q(Q(payments__term=term) & Q(payments__status=status))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def students_report(request):
    params = request.query_params

    queryset = Student.objects.filter(
        filter_by_gender(params.get('gender'))
        & filter_by_organization(params.get('organization'))
        & filter_by_institution(params.get('institution'))
        & filter_students_by_grade_level(params.get('level'))
        & filter_students_by_class(params.get('_class'))
        & filter_students_by_subject(params.get('subject'))
        & filter_students_by_student_type(params.get('student_type'))
        & filter_students_by_payments(params.get('payment_term'), params.get('payment_status'))
    )

    students_count = queryset.count()

    if params.get('data'):
        students = StudentReadSerializer(queryset, many=True).data
        return success_w_data(data={
            'count': students_count,
            'students': students
        })

    return success_w_data(data={
        'count': students_count,
    })


def filter_teachers_by_subject(subject):
    if subject is None:
        return Q()
    return Q(subject_classes__subject=subject)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teachers_report(request):
    params = request.query_params

    queryset = Employee.objects.filter(
        Q(is_teacher=True)
        & filter_by_organization(params.get('organization'))
        & filter_by_institution(params.get('institution'))
        & filter_teachers_by_subject(params.get('subject'))
    )

    teachers_count = queryset.count()
    if params.get('data'):
        teachers = EmployeeReadSerializer(queryset, many=True).data

        return success_w_data(data={
            'count': teachers_count,
            'teachers': teachers
        })

    return success_w_data(data={
        'count': teachers_count,
    })


def filter_attendance_or_result_by_organization(organization):
    if organization is None:
        return Q()
    return Q(student__institution__organization=organization)


def filter_attendance_or_result_by_institution(institution):
    if institution is None:
        return Q()
    return Q(student__institution=institution)


def filter_attendance_by_subject(subject):
    if subject is None:
        return Q()
    return Q(lesson__period__class_subject__subject=subject)


def filter_attendance_or_result_by_level(level):
    if level is None:
        return Q()
    return Q(student__grade__level=level)


def filter_attendance_or_result_by_grade(grade):
    if grade is None:
        return Q()
    return Q(student__grade__level=grade)


def filter_by_term(term):
    if term is None:
        return Q()
    return Q(term=term)


def filter_attendance_by_date_range(start, end):
    if start and end is not None:
        return Q(lesson__date__range=[start, end])
    return Q()


def filter_attendance_by_class(_class):
    if _class is None:
        return Q()
    return Q(lesson__period__class_subject___class=_class)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_report(request):
    params = request.query_params

    queryset = Attendance.objects.filter(
        filter_attendance_or_result_by_organization(params.get('organization'))
        & filter_attendance_or_result_by_institution(params.get('institution'))
        & filter_attendance_by_subject(params.get('subject'))
        & filter_attendance_or_result_by_level(params.get('level'))
        & filter_attendance_or_result_by_grade(params.get('grade'))
        & filter_by_term(params.get('term'))
        & filter_attendance_by_date_range(params.get('start'), params.get('end'))
        & filter_attendance_by_class(params.get('_class'))
    )

    attendance_count = queryset.count()

    if params.get('data'):
        attendance = AttendanceReadSerializer(queryset, many=True).data

        return success_w_data(data={
            'count': attendance_count,
            'attendance': attendance
        })

    return success_w_data(data={
        'count': attendance_count,
    })


GRADE_LIST = ['A', 'B', 'C', 'D', 'E', 'F']


def filter_results_by_subject(subject):
    if subject is None:
        return Q()
    return Q(class_subject__subject=subject)


def filter_results_by_class(_class):
    if _class is None:
        return Q()
    return Q(class_subject___class=_class)


def filter_results_by_student(student):
    if student is None:
        return Q()
    return Q(student=student)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_summary(request):
    params = request.query_params

    queryset = TermResult.objects.filter(
        filter_attendance_or_result_by_organization(params.get('organization'))
        & filter_attendance_or_result_by_institution(params.get('institution'))
        & filter_by_term(params.get('term'))
        & filter_attendance_or_result_by_level(params.get('level'))
        & filter_results_by_subject(params.get('subject'))
        & filter_results_by_class(params.get('_class'))
    )

    results = []

    print(queryset.count())

    for grade in GRADE_LIST:
        count = queryset.filter(grade__iexact=grade).count()
        results.append({
            'grade': grade,
            'count': count
        })

    return success_w_data(data=results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_result_reports(request):
    params = request.query_params

    queryset = TermResult.objects.filter(
        filter_attendance_or_result_by_organization(params.get('organization'))
        & filter_attendance_or_result_by_institution(params.get('institution'))
        & filter_by_term(params.get('term'))
        & filter_attendance_or_result_by_level(params.get('level'))
        & filter_results_by_subject(params.get('subject'))
        & filter_results_by_class(params.get('_class'))
        & filter_results_by_student(params.get('student'))
    ).order_by('-total_marks')

    results = TermResultReadSerializer(queryset, many=True).data

    return success_w_data(data=results)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_publishers_last_10_days_sales(request):
    publisher = request.query_params.get('publisher')

    current_date = timezone.now().date()
    start_date = current_date - timedelta(days=9)

    results = []

    for i in range(10):
        date = start_date + timedelta(days=i)
        queryset = BookPurchase.objects.filter(
            purchase_date__day=date.day,
            purchase_date__month=date.month,
            purchase_date__year=date.year,
            book__publisher=publisher,
        )
        total_sales = queryset.aggregate(Sum('total_price'))['total_price__sum'] or 0

        unit_sold = queryset.count()

        results.append({
            'date': date,
            'total_sales': total_sales,
            'unit_sold': unit_sold
        })

    return success_w_data(data=results)
