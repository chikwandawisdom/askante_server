# Generated by Django 5.0.4 on 2024-06-30 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book_shop', '0007_publisher_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='isbn_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
