import datetime
from datetime import datetime as dt

from django.db import models
from django.db.models import Q
from rest_framework import serializers

from institutions.models.institution import Institution
from institutions.models.organization import Organization
from institutions.models.terms import Terms
from students.models.students import Student


class Payment(models.Model):
    status_choices = (
        ('paid', 'Paid'),
        ('due', 'Due'),
        ('void', 'Void'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    charges = models.JSONField()
    amount = models.PositiveIntegerField()
    date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=status_choices, default='due')
    term = models.ForeignKey(Terms, on_delete=models.PROTECT, null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.student} - {self.date} - {self.amount}'


class PaymentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        depth = 1


def filter_by_institution(institution) -> Q:
    if institution is None:
        return Q()
    return Q(institution=institution)


def filter_by_student(student) -> Q:
    if student is None:
        return Q()
    return Q(student=student)


def filter_by_date_range(start, end):
    """
    :param start: start date
    :param end: end date
    :return: Q(query)
    """
    if start and end is not None:

        if start == end:
            date = start.split('-')
            return Q(date__year=date[0], date__month=date[1], date__day=date[2])
        else:
            from_date = dt.strptime(start, '%Y-%m-%d').date()
            # combine `from_date` with min time value (00:00)
            from_date = datetime.datetime.combine(from_date, datetime.time.min)
            # combine `from_date` with max time value (23:59:99) to have end date
            to_date = dt.strptime(end, '%Y-%m-%d').date()
            to_date = datetime.datetime.combine(to_date, datetime.time.max)

            # print(from_date, ' From')
            # print(to_date, ' To')
            return Q(date__range=[from_date, to_date])
    else:
        return Q()
