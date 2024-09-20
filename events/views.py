from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, get_paginated_response, \
    err_w_msg
from fundamentals.common_queries import search_by_name, filter_by_institution
from fundamentals.common_queries import search_by_name
from .models.activity import Activity, ActivityReadSerializer, ActivityWriteSerializer
from .models.age_group import AgeGroupReadSerializer, AgeGroupWriteSerializer, AgeGroup, filter_by_grade
from employees.models.employees import Employee
from students.models.students import Student, StudentReadSerializer
from .models.age_group_activity import AgeGroupActivity, AgeGroupActivityReadSerializer, AgeGroupActivityWriteSerializer
from events.models.activity_timetables import ActivityPeriod, ActivityPeriodReadSerializer, ActivityPeriodWriteSerializer
from institutions.methods.academic_year import get_active_academic_year
from .models.event import Event, EventReadSerializer, EventWriteSerializer
from users.permissions import IsTeacher


class ActivityList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        activitys = Activity.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('-id')
        serializer = ActivityReadSerializer(activitys, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = ActivityWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class ActivityDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        Activity = Activity.objects.filter(pk=pk).first()

        if not Activity:
            return success_w_msg('Activity not found.', status=HTTP_404_NOT_FOUND)

        serializer = ActivityReadSerializer(Activity)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        activity = Activity.objects.filter(pk=pk).first()

        if not activity:
            return success_w_msg('Activity not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()

        serializer = ActivityWriteSerializer(activity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        activity = Activity.objects.filter(pk=pk).first()

        if not activity:
            return success_w_msg('Activity not found.', status=HTTP_404_NOT_FOUND)

        activity.delete()
        return success_w_msg('Activity deleted successfully.')



class AgeGroupList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        age_groups = AgeGroup.objects.filter(
            Q(institution__organization=request.user.organization)
            & search_by_name(request.query_params.get('search'))
            & filter_by_institution(request.query_params.get('institution'))
            & filter_by_grade(request.query_params.get('grade'))
        ).order_by('-id')
        serializer = AgeGroupReadSerializer(age_groups, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = AgeGroupWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)


class AgeGroupDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        age_group = AgeGroup.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group:
            return success_w_msg('Age group not found.', status=HTTP_404_NOT_FOUND)

        serializer = AgeGroupReadSerializer(age_group)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        age_group = AgeGroup.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group:
            return success_w_msg('Age group not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = age_group.institution.id

        if data.get('class_teacher'):
            teacher = Employee.objects.filter(pk=data.get('class_teacher')).first()
            if not teacher:
                return success_w_msg('Teacher not found.', status=HTTP_404_NOT_FOUND)

            try:
                if teacher.is_teacher is False:
                    return success_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)
            except AttributeError:
                return success_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)

        serializer = AgeGroupWriteSerializer(age_group, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        age_group = AgeGroup.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group:
            return success_w_msg('Age group not found.', status=HTTP_404_NOT_FOUND)

        age_group.delete()
        return success_w_msg('Age group deleted successfully.')
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_students_to_age_group(request):
    data = request.data.copy()

    age_group = AgeGroup.objects.filter(pk=data['age_group'], institution__organization=request.user.organization).first()
    if not age_group:
        return success_w_msg('Age Group not found.', status=HTTP_404_NOT_FOUND)

    students = data.get('students')

    # add students to class
    age_group.students.add(*students)

    return success_w_msg('Students added to class successfully.')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_students_in_age_group(request):
    age_group_id = request.query_params.get('age_group')
    age_group = AgeGroup.objects.filter(pk=age_group_id, institution__organization=request.user.organization).first()

    if not age_group:
        return success_w_msg('Age Group not found.', status=HTTP_404_NOT_FOUND)

    students = age_group.students.all()
    serializer = StudentReadSerializer(students, many=True)
    return success_w_data(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_student_from_age_group(request):
    data = request.data.copy()

    try:
        age_group = AgeGroup.objects.filter(pk=data['age_group'], institution__organization=request.user.organization).first()
        if not age_group:
            return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

        student = data['student']

        # remove students from class
        age_group.students.remove(student)

    except KeyError:
        return success_w_msg('age_group is required.')

    return success_w_msg('Student removed from class successfully.')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_students_to_age_group(request):
    data = request.data.copy()

    age_group = AgeGroup.objects.filter(pk=data['age_group'], institution__organization=request.user.organization).first()
    if not age_group:
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

    students = data.get('students')

    # add students to class
    age_group.students.add(*students)

    return success_w_msg('Students added to class successfully.')



class AgeGroupActivityList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params

        if params.get('age_group') is None:
            return success_w_msg('age_group is required.')

        age_group_activities = AgeGroupActivity.objects.filter(
            Q(institution__organization=request.user.organization)
            & Q(age_group=params.get('age_group'))
        ).order_by('-id')
  
        serializer = AgeGroupActivityReadSerializer(age_group_activities, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = AgeGroupActivityWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data, status=201)
        return err_w_serializer(serializer.errors)



class AgeGroupActivityDetails(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        age_group_activity = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group_activity:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        serializer = AgeGroupActivityReadSerializer(age_group_activity)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        age_group_activity = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group_activity:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = age_group_activity.institution.id

        if data.get('teacher'):
            teacher = Employee.objects.filter(pk=data.get('teacher')).first()
            if not teacher:
                return success_w_msg('Teacher not found.', status=HTTP_404_NOT_FOUND)

            try:
                if teacher.is_teacher is False:
                    return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)
            except AttributeError:
                return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)

        serializer = AgeGroupActivityWriteSerializer(age_group_activity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        age_group_activity = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not age_group_activity:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        age_group_activity.delete()
        return success_w_msg('Age Group Activity deleted successfully.')
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_activity_period(request):
    data = request.data.copy()

    age_group_activity = AgeGroupActivity.objects.filter(pk=data['age_group_activity'],
                                                institution__organization=request.user.organization).first()
    data['institution'] = age_group_activity.institution.id
    if not age_group_activity:
        return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

    serializer = ActivityPeriodWriteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data, status=201)
    return err_w_serializer(serializer.errors)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_activity_period(request, pk):
    period = ActivityPeriod.objects.filter(pk=pk).first()

    if not period:
        return success_w_msg('Activity Period not found.', status=HTTP_404_NOT_FOUND)

    data = request.data.copy()

    serializer = ActivityPeriodWriteSerializer(period, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return success_w_data(serializer.data)
    return err_w_serializer(serializer.errors)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_activity_periods_of_a_class(request):
    age_group = request.query_params.get('age_group')
    if age_group is None:
        return success_w_msg('age_group is required.')

    age_group = AgeGroup.objects.filter(id=age_group, institution__organization=request.user.organization).first()

    if age_group is None:
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

    periods = ActivityPeriod.objects.select_related('age_group_activity').filter(age_group_activity__age_group=age_group)
    periods = ActivityPeriodReadSerializer(periods, many=True)

    return success_w_data(periods.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_activity_period(request, pk):
    period = ActivityPeriod.objects.filter(pk=pk, age_group_activity__institution__organization=request.user.organization).first()

    if not period:
        return success_w_msg('Period not found.', status=HTTP_404_NOT_FOUND)

    period.delete()
    return success_w_msg('Period deleted successfully.')



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_monthly_events_calendar(request):
    params = request.query_params

    # employee = Employee.objects.get(user=request.user)
    # active_academic_year = get_active_academic_year(employee.institution)

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
            ActivityPeriod.objects.select_related(
                "age_group_activity__age_group", "age_group_activity__activity", 
            )
            .filter(
                # Q(class_subject__teacher__user=request.user)& 
                Q(institution__organization=request.user.organization) &
                filter_by_period_day(current_date.strftime("%A"))
            )
            .order_by("period")
        )
        for period in periods:
            events.append(
                {
                    "type": "activity",
                    "id": period.id,
                    "title": f"{period.age_group_activity.age_group.name} - ({period.start} - {period.end})",
                    "subject": period.age_group_activity.activity.name,
                }
            )

        # events
        events_list = Event.objects.filter(
            # Q(class_subject__teacher__user=request.user)
            Q(organization=request.user.organization)
            & Q(
                date__day=current_date.day,
                date__month=current_date.month,
                date__year=current_date.year,
            )
        ).order_by("date")

        for event in events_list:
            events.append(
                {
                    "type": event.type,
                    "id": event.id,
                    "title": f'{event.title} - ({event.start} - {event.end})',
                    "activity": ''
                }
            )

        day["events"] = events
        monthly_calendar.append(day)

        current_date += timedelta(days=1)

    return success_w_data(
        data=monthly_calendar, msg="Monthly calendar fetched successfully"
    )


def filter_by_period_day(day):
    """
    Filter periods by day
    :param day: day
    :return: Q()
    """
    if day is not None:
        return Q(day=day)
    return Q()


class EventList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        serializer = EventWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Event added successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def get(request):
        params = request.query_params
        # active_academic_year = get_active_academic_year(employee.institution)

        events = Event.objects.filter(
            Q(organization=request.user.organization) 
            # & filter_by_academic_year(active_academic_year)
        ).order_by("-id")

        events = EventReadSerializer(events, many=True).data

        return success_w_data(data=events, msg="Events fetched successfully")


class EventDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        event = Event.objects.get(id=pk)
        event = EventReadSerializer(event).data
        return success_w_data(data=event, msg="Event fetched successfully")

    @staticmethod
    def patch(request, pk):
        event = Event.objects.get(id=pk)
        serializer = EventWriteSerializer(instance=event, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg(msg="Event updated successfully")
        return err_w_msg(msg=serializer.errors)

    @staticmethod
    def delete(request, pk):
        event = Event.objects.get(id=pk)
        event.delete()
        return success_w_msg(msg="Event deleted successfully")
    


def filter_by_academic_year(academic_year):
    """
    Filter periods by academic year
    :param academic_year: pk
    :return: Q()
    """
    if academic_year is not None:
        return Q(academic_year=academic_year)
    return Q()


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_teachers_age_group_list(request):
    employee = Employee.objects.get(user=request.user)

    age_group_activities = AgeGroupActivity.objects.filter(teacher=employee).order_by("-id")
    age_group_activities = AgeGroupActivityReadSerializer(age_group_activities, many=True).data

    return success_w_data(data=age_group_activities, msg="Class list fetched successfully")


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsTeacher])
def get_teachers_activity_periods(request):
    params = request.query_params

    periods = ActivityPeriod.objects.filter(
        Q(class_subject__teacher__user=request.user)
        & filter_by_age_group_activity(params.get("age_group_activity"))
        & filter_by_period_day(params.get("day"))
    ).order_by("day", "period")
    periods = ActivityPeriodReadSerializer(periods, many=True).data

    return success_w_data(data=periods, msg="Periods fetched successfully")


def filter_by_age_group_activity(age_group_activity):
    """
    Filter periods by class subject
    :param age_group_activity: pk
    :return: Q()
    """
    if age_group_activity is not None:
        return Q(age_group_activity=age_group_activity)
    return Q()
