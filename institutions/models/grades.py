from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution
from institutions.models.levels import Level


class Grade(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='active', choices=status_choices)
    level = models.ForeignKey(Level, on_delete=models.PROTECT, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class GradeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class GradeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
