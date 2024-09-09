from django.db import models
from rest_framework import serializers

from institutions.models.organization import Organization


class ChargeType(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=status_choices, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name


class ChargeTypeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeType
        fields = '__all__'


class ChargeTypeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeType
        fields = '__all__'
