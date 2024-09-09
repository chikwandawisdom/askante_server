from django.db import models
from django.utils import timezone
from rest_framework import serializers


class Organization(models.Model):
    name = models.CharField(max_length=255)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=100.00)
    payment_frequency = models.PositiveIntegerField(default=1) # months
    next_payment_date = models.DateField(null=True, blank=True, default=timezone.now)
    last_invoice_generated = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.id}'


class OrganizationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'


class OrganizationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
