from django.db import models
from rest_framework import serializers
from django.contrib.postgres.fields import ArrayField

from academic.models.marking_criteria import MarkingCriterion, MarkingCriterionReadSerializer
from institutions.models.academic_years import AcademicYear
from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer
from institutions.models.terms import Terms


class Assignment(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    links = models.JSONField()
    due_date = models.DateTimeField()
    marking_criterion = models.ForeignKey(MarkingCriterion, on_delete=models.PROTECT)
    max_marks = models.PositiveIntegerField()
    attachments = ArrayField(models.TextField(), blank=True, null=True)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AssignmentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentReadSerializer(serializers.ModelSerializer):
    class_subject = ClassSubjectReadSerializer(read_only=True, many=False)
    marking_criterion = MarkingCriterionReadSerializer(read_only=True, many=False)

    class Meta:
        model = Assignment
        fields = '__all__'
