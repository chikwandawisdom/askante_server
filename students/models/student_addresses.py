from django.db import models
from rest_framework import serializers

from students.models.students import Student


class StudentAddress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    label = models.CharField(max_length=20)
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class StudentAddressWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAddress
        fields = '__all__'


class StudentAddressReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAddress
        fields = '__all__'
