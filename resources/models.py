from django.db import models
from rest_framework import serializers

from institutions.models.grades import Grade
from institutions.models.levels import Level
from institutions.models.subjects import Subject
from users.models import User
from users.serializers import UserSerializer
from institutions.models.organization import Organization, OrganizationReadSerializer


class Resource(models.Model):

    type_choices = (
        ('past_exam', 'past-exam'),
        ('notes', 'notes'),
        ('article', 'article'),
        ('other', 'other'),
    )

    syllabus_choices = (
        ('zimsec', 'ZIMSEC'),
        ('cambridge', 'cambridge'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    resource_url = models.TextField(max_length=1000)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    type = models.CharField(max_length=10, choices=type_choices)
    syllabus = models.CharField(max_length=10, choices=syllabus_choices)
    posted_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResourceWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'


class ResourceReadSerializer(serializers.ModelSerializer):
    posted_by = UserSerializer()
    organization = OrganizationReadSerializer()
    class Meta:
        model = Resource
        fields = (
            "name", 
            "description", 
            "grade", 
            "subject", 
            "posted_by", 
            "id",
            "level", 
            "type",
            "syllabus",
            "resource_url",
            "organization",
            "created_at", 
        )