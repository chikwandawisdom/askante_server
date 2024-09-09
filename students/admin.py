from django.contrib import admin

from .models.student_types import StudentType
from .models.students import Student

admin.site.register(Student)
admin.site.register(StudentType)
