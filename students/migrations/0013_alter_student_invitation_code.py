# Generated by Django 5.0.4 on 2024-05-09 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0012_alter_student_invitation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='invitation_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
