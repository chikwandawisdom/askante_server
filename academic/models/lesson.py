from django.db import models
from rest_framework import serializers

from institutions.models.academic_years import AcademicYear
from institutions.models.terms import Terms
from institutions.models.timetables import Period
from registry.models.attendance_group import AttendanceGroup, AttendanceGroupReadSerializer
from students.models.students import Student, StudentReadSerializer


class Lesson(models.Model):
    period = models.ForeignKey(Period, on_delete=models.CASCADE)
    date = models.DateField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)


class Attendance(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance_group = models.ForeignKey(AttendanceGroup, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AttendanceReadSerializer(serializers.ModelSerializer):
    student = StudentReadSerializer(read_only=True, many=False)
    attendance_group = AttendanceGroupReadSerializer(read_only=True, many=False)

    class Meta:
        model = Attendance
        fields = '__all__'
