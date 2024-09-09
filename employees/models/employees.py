from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from employees.models.employment_positions import EmploymentPosition
from employees.models.employment_types import EmploymentType
from institutions.models.institution import Institution
from institutions.models.organization import Organization
from users.models import User


class Employee(models.Model):
    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    )

    special_role_choices = (
        ('bursar', 'bursar'),
        ('librarian', 'librarian'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=gender_choices)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    citizenship = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    invitation_code = models.CharField(max_length=50, null=True, blank=True)
    dp = models.URLField(null=True, blank=True)
    archived = models.BooleanField(default=False)

    # employment position related fields
    employee_id = models.CharField(max_length=50, null=True, blank=True)
    employment_position = models.ForeignKey(EmploymentPosition, on_delete=models.CASCADE, null=True, blank=True)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.CASCADE, null=True, blank=True)
    is_teacher = models.BooleanField(default=False)
    special_role = models.CharField(max_length=50, null=True, blank=True, choices=special_role_choices)
    employment_start_date = models.DateField(null=True, blank=True)
    employment_end_date = models.DateField(null=True, blank=True)

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Custom validation to ensure uniqueness of employee_id within an organization
        if self.employee_id:
            existing_employees_with_same_id = Employee.objects.filter(institution__organization=self.institution.organization,
                                                                      employee_id=self.employee_id).exclude(id=self.id)
            if existing_employees_with_same_id.exists():
                raise ValidationError("Employee ID must be unique within the organization.")
        super().save(*args, **kwargs)


class EmployeeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        depth = 1
