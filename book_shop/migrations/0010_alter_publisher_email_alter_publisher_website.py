# Generated by Django 4.0.2 on 2024-08-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0009_book_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publisher',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='publisher',
            name='website',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
