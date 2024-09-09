from django.db import models
from rest_framework import serializers

from employees.models.employees import Employee


class EmployeeContact(models.Model):
    type_choices = (
        ('phone', 'phone'),
        ('email', 'email'),
    )

    label = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, choices=type_choices)
    value = models.CharField(max_length=50)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EmployeeContactWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeContact
        fields = '__all__'


class EmployeeContactReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeContact
        fields = '__all__'
