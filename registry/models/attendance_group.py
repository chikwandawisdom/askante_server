from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution


class AttendanceGroup(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    record_late_time = models.BooleanField(default=False)
    color = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=status_choices, default='active')

    def __str__(self):
        return f'{self.id}-{self.name}'


class AttendanceGroupWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceGroup
        fields = '__all__'


class AttendanceGroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceGroup
        fields = '__all__'
