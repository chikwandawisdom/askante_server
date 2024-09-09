from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution


class Level(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}'


class LevelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'


class LevelReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = '__all__'
