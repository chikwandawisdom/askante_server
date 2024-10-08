# Generated by Django 5.0.4 on 2024-04-27 21:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('institutions', '0017_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('record_late_time', models.BooleanField(default=False)),
                ('color', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
        ),
    ]
