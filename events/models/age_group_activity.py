from django.db import models
from rest_framework import serializers

from employees.models.employees import Employee, EmployeeReadSerializer
from events.models.age_group import AgeGroup, AgeGroupReadSerializer
from institutions.models.institution import Institution
from institutions.models.subjects import Subject, SubjectReadSerializer
from events.models.activity import Activity, ActivityReadSerializer


class AgeGroupActivity(models.Model):
    age_group = models.ForeignKey(AgeGroup, on_delete=models.CASCADE, related_name='age_group_activities')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='activity_age_groups')

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AgeGroupActivityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeGroupActivity
        fields = '__all__'


class AgeGroupActivityReadSerializer(serializers.ModelSerializer):
    _class = AgeGroupReadSerializer(read_only=True, many=False)
    subject = ActivityReadSerializer(read_only=True, many=False)
    teacher = EmployeeReadSerializer(read_only=True, many=False)

    class Meta:
        model = AgeGroupActivity
        fields = '__all__'
