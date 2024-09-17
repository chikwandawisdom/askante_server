from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, get_paginated_response, \
    err_w_msg
from fundamentals.common_queries import search_by_name
from .models.activity import Activity, ActivityReadSerializer, ActivityWriteSerializer
from rest_framework.permissions import IsAuthenticated


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
