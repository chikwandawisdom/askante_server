from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta

from fundamentals.common_queries import search_by_name
from .models.attendance_group import AttendanceGroup, AttendanceGroupWriteSerializer, AttendanceGroupReadSerializer
from .models.announcements import Announcement, AnnouncementReadSerializer, AnnouncementWriteSerializer
from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, err_w_msg


class AttendanceGroupListView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        attendance_groups = AttendanceGroup.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('name')
        serializer = AttendanceGroupReadSerializer(attendance_groups, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        serializer = AttendanceGroupWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Attendance Group created successfully.')
        return err_w_serializer(serializer)


class AttendanceGroupDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        attendance_group = AttendanceGroup.objects.filter(id=pk).first()
        if not attendance_group:
            return err_w_msg('Attendance Group not found.')
        serializer = AttendanceGroupReadSerializer(attendance_group)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):

        attendance_group = AttendanceGroup.objects.filter(id=pk).first()
        if not attendance_group:
            return err_w_msg('Attendance Group not found.')

        serializer = AttendanceGroupWriteSerializer(attendance_group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Attendance Group updated successfully.')
        return err_w_serializer(serializer)

    @staticmethod
    def delete(request, pk):
        attendance_group = AttendanceGroup.objects.filter(id=pk).first()
        if not attendance_group:
            return err_w_msg('Attendance Group not found.')
        attendance_group.delete()
        return success_w_msg('Attendance Group deleted successfully.')
    

class AnnouncementDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        announcement = Announcement.objects.filter(id=pk).first()
        if not announcement:
            return err_w_msg('Announcement not found.')
        serializer = AnnouncementReadSerializer(announcement)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):

        announcement = Announcement.objects.filter(id=pk).first()
        if not announcement:
            return err_w_msg('Announcement not found.')

        serializer = AnnouncementWriteSerializer(announcement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Announcement updated successfully.')
        return err_w_serializer(serializer)

    @staticmethod
    def delete(request, pk):
        announcement = Announcement.objects.filter(id=pk).first()
        if not announcement:
            return err_w_msg('Announcement not found.')
        announcement.delete()
        return success_w_msg('Announcement deleted successfully.')
    


class AnnouncementListView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        announcements = Announcement.objects.filter(
            search_by_name(request.query_params.get('search'))
        ).order_by('created_at')
        serializer = AnnouncementReadSerializer(announcements, many=True)
        return success_w_data(serializer.data)

    @staticmethod
    def post(request):
        data = request.data
        data['posted_by'] = request.user.id
        # checking if due_date is in the past. parse the due_date first which is a YYYY-MM-DDTHH:MM:SS.sssZ string
        expiry_date = datetime.strptime(data["expiry_date"], "%Y-%m-%d")
        if expiry_date < datetime.now():
            return err_w_msg(msg="Expiry date cannot be in the past")
        serializer = AnnouncementWriteSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Announcement created successfully.')
        return err_w_serializer(serializer)

