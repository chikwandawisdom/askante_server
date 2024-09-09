from django.db import models
from rest_framework import serializers

from students.models.students import Student


class StudentContact(models.Model):
    type_choices = (
        ('phone', 'phone'),
        ('email', 'email'),
    )

    person = models.CharField(max_length=100, null=False, blank=False)
    label = models.CharField(max_length=20, null=True, blank=True)
    type = models.CharField(max_length=20, choices=type_choices)
    value = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class StudentContactWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentContact
        fields = '__all__'


class StudentContactReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentContact
        fields = '__all__'
