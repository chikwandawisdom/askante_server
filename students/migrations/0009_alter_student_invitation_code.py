# Generated by Django 5.0.4 on 2024-05-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_student_user_alter_student_invitation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='invitation_code',
            field=models.CharField(blank=True, default='U5U-lH_4uM_zHv0tO1eG', max_length=50, null=True),
        ),
    ]
