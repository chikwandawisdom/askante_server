# Generated by Django 5.0.4 on 2024-04-07 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_employee_dp'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
