# Generated by Django 4.0.2 on 2024-09-20 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0034_alter_organization_next_payment_date'),
        ('events', '0005_activityperiod_institution'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date', models.DateTimeField()),
                ('type', models.CharField(choices=[('academic', 'academic'), ('extracurricular', 'extracurricular'), ('social', 'social'), ('other', 'other')], max_length=100)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.academicyear')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('term', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.terms')),
            ],
        ),
    ]
