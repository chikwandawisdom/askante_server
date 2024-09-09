from django.db import models
from rest_framework import serializers

from academic.models.marking_criteria import MarkingCriterion
from institutions.models.academic_years import AcademicYear
from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer
from institutions.models.terms import Terms


class Exam(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=100)
    marking_criterion = models.ForeignKey(MarkingCriterion, on_delete=models.PROTECT)
    max_marks = models.PositiveIntegerField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)
    start = models.TimeField()
    end = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ExamWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class ExamReadSerializer(serializers.ModelSerializer):
    class_subject = ClassSubjectReadSerializer(read_only=True, many=False)

    class Meta:
        model = Exam
        fields = '__all__'
