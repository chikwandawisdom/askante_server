from django.db import models
from rest_framework import serializers


class Terms(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    status = models.CharField(max_length=8, default='active', choices=status_choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.name}'


class TermsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'


class TermsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = '__all__'
