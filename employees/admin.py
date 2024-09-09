from django.contrib import admin

from .models.employment_positions import EmploymentPosition
from .models.employment_types import EmploymentType
from .models.employees import Employee

admin.site.register(EmploymentPosition)
admin.site.register(EmploymentType)
admin.site.register(Employee)
