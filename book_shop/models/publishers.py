from django.db import models

from rest_framework import serializers


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    website = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PublisherWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class PublisherReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'
