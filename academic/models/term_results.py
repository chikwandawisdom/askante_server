from django.db import models

from rest_framework import serializers

from institutions.models.academic_years import AcademicYear
from institutions.models.class_subjects import ClassSubject
from institutions.models.terms import Terms
from students.models.students import Student


class TermResult(models.Model):
    term = models.ForeignKey(Terms, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    total_marks = models.PositiveIntegerField()
    grade = models.CharField(max_length=10)
    notes = models.CharField(max_length=3000, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TermResultWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermResult
        fields = '__all__'


class TermResultReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermResult
        fields = '__all__'
        depth = 1