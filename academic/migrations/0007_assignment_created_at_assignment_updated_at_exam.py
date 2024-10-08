# Generated by Django 5.0.4 on 2024-05-09 16:12

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0006_alter_assignment_attachments'),
        ('institutions', '0019_alter_class_students_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='assignment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('type', models.CharField(max_length=100)),
                ('max_marks', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('class_subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.classsubject')),
                ('marking_criterion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='academic.markingcriterion')),
            ],
        ),
    ]
