from django.db import models
from rest_framework import serializers

from employees.models.employees import Employee, EmployeeReadSerializer
from institutions.models.classes import Class, ClassReadSerializer
from institutions.models.institution import Institution
from institutions.models.subjects import Subject, SubjectReadSerializer


class ClassSubject(models.Model):
    _class = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    period_per_week_official = models.PositiveIntegerField(null=True, blank=True)
    period_per_week_timetable = models.PositiveIntegerField(null=True, blank=True)
    period_per_week_report = models.PositiveIntegerField(null=True, blank=True)
    passing_mark = models.PositiveIntegerField(null=True, blank=True)
    teacher = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='subject_classes')

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClassSubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSubject
        fields = '__all__'


class ClassSubjectReadSerializer(serializers.ModelSerializer):
    _class = ClassReadSerializer(read_only=True, many=False)
    subject = SubjectReadSerializer(read_only=True, many=False)
    teacher = EmployeeReadSerializer(read_only=True, many=False)

    class Meta:
        model = ClassSubject
        fields = '__all__'
