from rest_framework.urls import path

from .views import AttendanceGroupListView, AttendanceGroupDetailView, AnnouncementDetailView, AnnouncementListView

urlpatterns = [
    path('attendance-groups', AttendanceGroupListView.as_view(), name='attendance-group-list'),
    path('attendance-groups/<int:pk>', AttendanceGroupDetailView.as_view(), name='attendance-group-detail'),
    path('announcements', AnnouncementListView.as_view(), name='announcement-list'),
    path('announcements/<int:pk>', AnnouncementDetailView.as_view(), name='announcement-detail'),
]
