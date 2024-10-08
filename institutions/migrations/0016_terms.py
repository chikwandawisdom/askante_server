# Generated by Django 5.0.4 on 2024-04-27 00:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0015_rename_teacher_class_class_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Terms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=10)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
            ],
        ),
    ]
