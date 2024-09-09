from django.db import models
from rest_framework import serializers

from institutions.models.academic_years import AcademicYear
from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer


class MarkingCriterion(models.Model):
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField()
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)


class MarkingCriterionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingCriterion
        fields = '__all__'


class MarkingCriterionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingCriterion
        fields = '__all__'
