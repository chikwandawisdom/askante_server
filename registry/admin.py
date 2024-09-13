from django.contrib import admin

from .models.attendance_group import AttendanceGroup
from .models.announcements import Announcement

admin.site.register(AttendanceGroup)
admin.site.register(Announcement)
