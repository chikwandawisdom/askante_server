from django.db import models
from rest_framework import serializers

from institutions.models.academic_years import AcademicYear
from institutions.models.terms import Terms
from institutions.models.institution import Institution
from institutions.models.organization import Organization


class Event(models.Model):

    type_choices = (
        ('academic', 'academic'),
        ('extracurricular', 'extracurricular'),
        ('social', 'social'),
        ('other', 'other'),
    )


    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    type = models.CharField(max_length=100, choices=type_choices)
    # academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE, null=True, blank=True)
    start = models.TimeField()
    end = models.TimeField()
    # institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class EventReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
