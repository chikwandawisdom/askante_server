from django.db import models
from django.db.models import Q
from rest_framework import serializers

from academic.models.marking_criteria import MarkingCriterion
from institutions.models.academic_years import AcademicYear
from institutions.models.class_subjects import ClassSubject
from institutions.models.terms import Terms
from students.models.students import Student


class Mark(models.Model):
    assessment_type_choices = (
        ('assignment', 'Assignment'),
        ('exam', 'Exam')
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=100, choices=assessment_type_choices)
    assessment_id = models.PositiveIntegerField()
    max_marks = models.PositiveIntegerField()
    marks = models.PositiveIntegerField()
    marking_criterion = models.ForeignKey(MarkingCriterion, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MarksWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'


class MarksReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'
        depth = 1


def filter_marks_by_student(student) -> Q:
    """
    Filter marks by student
    :param student: int | None
    :return: Q
    """
    if student:
        return Q(student=student)
    return Q()


def filter_marks_by_assessment_id(assessment_id: int) -> Q:
    """
    Filter marks by assessment id
    :param assessment_id: int | None
    :return: Q
    """
    if assessment_id:
        return Q(assessment_id=assessment_id)
    return Q()
