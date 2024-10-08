# Generated by Django 5.0.4 on 2024-05-09 06:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0003_markingcriterion'),
        ('institutions', '0019_alter_class_students_period'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('links', models.JSONField()),
                ('due_date', models.DateTimeField()),
                ('max_marks', models.PositiveIntegerField()),
                ('class_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.classsubject')),
                ('marking_criterion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.markingcriterion')),
            ],
        ),
    ]
