# Generated by Django 5.0.4 on 2024-06-30 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0030_organization_last_invoice_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='district',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='institution',
            name='province',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
