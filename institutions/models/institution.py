from django.db import models
from django.utils import timezone

from institutions.models.organization import Organization


class Institution(models.Model):
    status_choices = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, default='active', choices=status_choices)
    province = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='institutions')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.id}'
