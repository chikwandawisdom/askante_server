from django.db import models
from rest_framework import serializers

from students.models.students import Student


class Parent(models.Model):
    type_choices = (
        ('father', 'father'),
        ('mother', 'mother'),
        ('guardian', 'guardian'),
    )

    type = models.CharField(max_length=10, choices=type_choices)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    citizenship = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    occupation = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=False, blank=False)


class ParentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'


class ParentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = '__all__'
