from django.db import models
from django.db.models import Q
from rest_framework import serializers

from employees.models.employees import Employee, EmployeeReadSerializer
from institutions.models.grades import Grade, GradeReadSerializer
from institutions.models.institution import Institution
from students.models.students import Student, StudentReadSerializer


class AgeGroup(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    color = models.CharField(max_length=10)
    max_period_per_day = models.PositiveIntegerField(null=True, blank=True)
    students = models.ManyToManyField(Student, related_name='activitys') # Team
    class_teacher = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='activitys')

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class AgeGroupWriteSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True, required=False)
    class Meta:
        model = AgeGroup
        fields = '__all__'


class AgeGroupReadSerializer(serializers.ModelSerializer):
    grade = GradeReadSerializer(read_only=True)
    class_teacher = EmployeeReadSerializer(read_only=True, many=False)

    class Meta:
        model = AgeGroup
        fields = '__all__'


def filter_by_grade(grade):
    if grade:
        return Q(grade=grade)
    return Q()
