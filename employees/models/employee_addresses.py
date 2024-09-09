from django.db import models
from rest_framework import serializers

from employees.models.employees import Employee


class EmployeeAddress(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class EmployeeAddressWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = '__all__'


class EmployeeAddressReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = '__all__'
