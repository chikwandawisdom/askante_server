# Generated by Django 5.0.4 on 2024-06-03 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0022_academicyear_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicyear',
            name='completed',
        ),
    ]
