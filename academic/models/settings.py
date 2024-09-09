from django.db import models

from rest_framework import serializers


class Settings(models.Model):
    show_academic_year = models.BooleanField(default=True)

    def __str__(self):
        return "Settings"


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = "__all__"
