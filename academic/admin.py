from django.contrib import admin

from .models.lesson import Lesson, Attendance
from .models.term_results import TermResult

admin.site.register(Lesson)
admin.site.register(Attendance)
admin.site.register(TermResult)
