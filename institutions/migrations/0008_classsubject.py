# Generated by Django 5.0.4 on 2024-04-22 23:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0007_rename_colors_class_color_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period_per_week_official', models.PositiveIntegerField(blank=True, null=True)),
                ('period_per_week_timetable', models.PositiveIntegerField(blank=True, null=True)),
                ('period_per_week_report', models.PositiveIntegerField(blank=True, null=True)),
                ('passing_mark', models.PositiveIntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.subject')),
            ],
        ),
    ]
