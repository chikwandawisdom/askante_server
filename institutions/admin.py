from django.contrib import admin

from institutions.models.institution import Institution
from institutions.models.organization import Organization
from institutions.models.subjects import Subject
from institutions.models.class_subjects import ClassSubject
from institutions.models.academic_years import AcademicYear
from institutions.models.classes import Class
from institutions.models.timetables import Period
from institutions.models.terms import Terms
from institutions.models.levels import Level
from institutions.models.grades import Grade

admin.site.register(Organization)
admin.site.register(Institution)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(AcademicYear)
admin.site.register(Class)
admin.site.register(Period)
admin.site.register(Terms)
admin.site.register(Level)
admin.site.register(Grade)