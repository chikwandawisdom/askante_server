from django.db import models
from rest_framework import serializers

from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer


class Period(models.Model):
    day_choices = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )

    class_subject = models.ForeignKey(ClassSubject, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=day_choices)
    period = models.PositiveIntegerField()
    start = models.TimeField()
    end = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class_subject, day, start, end should be unique together
    class Meta:
        unique_together = ['class_subject', 'day', 'start', 'end']

    def __str__(self):
        return f'{self.start} - {self.end}'


class PeriodWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'


class PeriodReadSerializer(serializers.ModelSerializer):
    class_subject = ClassSubjectReadSerializer(read_only=True, many=False)

    class Meta:
        model = Period
        fields = '__all__'
