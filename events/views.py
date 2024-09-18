from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated

from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, get_paginated_response, \
    err_w_msg
from fundamentals.common_queries import search_by_name, filter_by_institution
from fundamentals.common_queries import search_by_name
from .models.activity import Activity, ActivityReadSerializer, ActivityWriteSerializer
from .models.age_group import AgeGroupReadSerializer, AgeGroupWriteSerializer, AgeGroup, filter_by_grade
from employees.models.employees import Employee
from students.models.students import Student, StudentReadSerializer
from .models.age_group_activity import AgeGroupActivity, AgeGroupActivityReadSerializer, AgeGroupActivityWriteSerializer


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
        return success_w_msg('Class not found.', status=HTTP_404_NOT_FOUND)

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
            return success_w_msg('_class is required.')

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
        class_subject = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        serializer = AgeGroupActivityReadSerializer(class_subject)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):
        class_subject = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['institution'] = class_subject.institution.id

        if data.get('teacher'):
            teacher = Employee.objects.filter(pk=data.get('teacher')).first()
            if not teacher:
                return success_w_msg('Teacher not found.', status=HTTP_404_NOT_FOUND)

            try:
                if teacher.is_teacher is False:
                    return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)
            except AttributeError:
                return err_w_msg('Employee is not a teacher.', status=HTTP_400_BAD_REQUEST)

        serializer = AgeGroupActivityWriteSerializer(class_subject, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        class_subject = AgeGroupActivity.objects.filter(pk=pk, institution__organization=request.user.organization).first()

        if not class_subject:
            return success_w_msg('Age Group Activity not found.', status=HTTP_404_NOT_FOUND)

        class_subject.delete()
        return success_w_msg('Age Group Activity deleted successfully.')

