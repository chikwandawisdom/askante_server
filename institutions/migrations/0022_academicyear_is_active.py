# Generated by Django 5.0.4 on 2024-06-03 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0021_grade_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='academicyear',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
