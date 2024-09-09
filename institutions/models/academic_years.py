from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution
from institutions.serializers import InstitutionReadSerializer


class AcademicYear(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AcademicYearWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'


class AcademicYearReadSerializer(serializers.ModelSerializer):
    institution = InstitutionReadSerializer(read_only=True, many=False)

    class Meta:
        model = AcademicYear
        fields = '__all__'
