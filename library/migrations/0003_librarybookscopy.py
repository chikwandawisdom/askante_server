# Generated by Django 5.0.4 on 2024-05-26 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0019_alter_class_students_period'),
        ('library', '0002_alter_librarybook_organization'),
        ('students', '0013_alter_student_invitation_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryBooksCopy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('copy_number', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('row', models.CharField(max_length=50)),
                ('check_out_date', models.DateTimeField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('check_in_date', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('available', 'Available'), ('checked_out', 'Checked Out')], default='available', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('current_lender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='students.student')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.institution')),
                ('library_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.librarybook')),
            ],
        ),
    ]
