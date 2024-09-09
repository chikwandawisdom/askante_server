from django.db import models
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from institutions.models.grades import Grade
from institutions.models.institution import Institution
from students.models.student_types import StudentType
from users.models import User


class Student(models.Model):
    gender_choices = (
        ('male', 'male'),
        ('female', 'female'),
        ('other', 'other'),
    )

    status_choices = (
        ('enrolled', 'enrolled'),
        ('graduated', 'graduated'),
        ('transferred', 'transferred'),
    )

    student_id = models.CharField(max_length=50, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=50)  # todo: change this to a foreign key
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    birth_place = models.CharField(max_length=50, null=True, blank=True)
    citizenship = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    registration_date = models.DateField(null=True, blank=True)
    register_number = models.CharField(max_length=50, null=True, blank=True)
    register_id = models.CharField(max_length=50, null=True, blank=True)
    language = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=50, null=False, blank=False, default='enrolled')
    dp = models.URLField(null=True, blank=True)
    student_type = models.ForeignKey(StudentType, on_delete=models.PROTECT, null=True, blank=True)

    # todo: new fields
    invitation_code = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='student_user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Custom validation to ensure uniqueness of student_id within an institution
        if self.student_id:
            existing_employees_with_same_id = Student.objects.filter(institution=self.institution,
                                                                     student_id=self.student_id).exclude(id=self.id)
            if existing_employees_with_same_id.exists():
                raise ValidationError("Student ID must be unique within the institution.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.first_name} {self.last_name}'


class StudentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class StudentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        depth = 1
