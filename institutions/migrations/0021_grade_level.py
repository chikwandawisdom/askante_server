# Generated by Django 5.0.4 on 2024-06-03 20:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0020_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='institutions.level'),
            preserve_default=False,
        ),
    ]
