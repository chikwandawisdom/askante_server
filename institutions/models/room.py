from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution


class Room(models.Model):
    status_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    floor_number = models.PositiveIntegerField(null=True, blank=True)
    number_of_seats = models.PositiveIntegerField(null=True, blank=True)
    number_of_computers = models.PositiveIntegerField(null=True, blank=True)
    has_projector = models.BooleanField(default=False)
    has_smart_board = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=status_choices, default='active')

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RoomWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
