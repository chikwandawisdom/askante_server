# Generated by Django 5.0.4 on 2024-05-09 07:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0005_assignment_attachments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='attachments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None),
        ),
    ]
