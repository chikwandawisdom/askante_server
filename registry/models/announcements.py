from django.db import models
from django.db.models import Q
from rest_framework import serializers

from institutions.models.organization import Organization
from users.models import User
from users.serializers import UserSerializer


class Announcement(models.Model):

    title = models.CharField(max_length=255, null=False, blank=False)
    body = models.TextField(max_length=5000, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    expiry_date = models.DateTimeField(null=True, blank=True)
    posted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AnnouncementWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'


class AnnouncementReadSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer()
    class Meta:
        model = Announcement
        # fields = '__all__'
        fields = ("title", "body", "organization", "expiry_date", "posted_by", "created_at", "id")

