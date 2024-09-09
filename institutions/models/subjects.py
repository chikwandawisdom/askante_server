from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution


class Subject(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    color = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=status_choices, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SubjectWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class SubjectReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
