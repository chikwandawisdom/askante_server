from django.db import models
from rest_framework import serializers

from finance.models.charge_types import ChargeType
from institutions.models.organization import Organization


class Charge(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )

    charge_type = models.ForeignKey(ChargeType, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=status_choices, default='active')
    price = models.PositiveIntegerField()

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChargeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = '__all__'


class ChargeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        exclude = ('organization',)
        depth = 1
