# Generated by Django 4.0.2 on 2024-08-24 10:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0033_alter_institution_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='next_payment_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
