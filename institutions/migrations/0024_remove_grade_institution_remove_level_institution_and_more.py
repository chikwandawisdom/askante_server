# Generated by Django 5.0.4 on 2024-06-17 03:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0023_remove_academicyear_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grade',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='level',
            name='institution',
        ),
        migrations.RemoveField(
            model_name='terms',
            name='institution',
        ),
    ]
