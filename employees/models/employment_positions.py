from django.db import models
from rest_framework import serializers

from institutions.models.organization import Organization


class EmploymentPosition(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    title = models.CharField(max_length=50)
    status = models.CharField(max_length=8, default='active', choices=status_choices)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class EmploymentPositionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentPosition
        fields = '__all__'


class EmploymentPositionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentPosition
        fields = '__all__'
