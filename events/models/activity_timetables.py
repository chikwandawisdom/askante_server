from django.db import models
from rest_framework import serializers

from institutions.models.class_subjects import ClassSubject, ClassSubjectReadSerializer
from events.models.age_group_activity import AgeGroupActivity, AgeGroupActivityReadSerializer


class ActivityPeriod(models.Model):
    day_choices = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    )

    age_group_activity = models.ForeignKey(AgeGroupActivity, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=day_choices)
    period = models.PositiveIntegerField()
    start = models.TimeField()
    end = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # age_group_activity, day, start, end should be unique together
    class Meta:
        unique_together = ['age_group_activity', 'day', 'start', 'end']

    def __str__(self):
        return f'{self.start} - {self.end}'


class ActivityPeriodWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityPeriod
        fields = '__all__'


class ActivityPeriodReadSerializer(serializers.ModelSerializer):
    age_group_activity = AgeGroupActivityReadSerializer(read_only=True, many=False)

    class Meta:
        model = ActivityPeriod
        fields = '__all__'
