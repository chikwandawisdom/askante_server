# Generated by Django 5.0.4 on 2024-06-23 18:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_payment_term'),
        ('students', '0015_student_student_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='students.student'),
        ),
    ]
