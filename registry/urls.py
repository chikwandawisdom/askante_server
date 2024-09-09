from rest_framework.urls import path

from .views import AttendanceGroupListView, AttendanceGroupDetailView

urlpatterns = [
    path('attendance-groups', AttendanceGroupListView.as_view(), name='attendance-group-list'),
    path('attendance-groups/<int:pk>', AttendanceGroupDetailView.as_view(), name='attendance-group-detail'),
]
