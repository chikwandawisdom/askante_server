from django.db import models
from rest_framework import serializers

from institutions.models.organization import Organization


class Invoice(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    is_paid = models.BooleanField(default=False)
    # token = models.CharField(max_length=250, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Invoice for {self.organization.name} - {self.id}'


class InvoicesReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1
