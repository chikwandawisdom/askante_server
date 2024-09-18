from django.contrib import admin

from .models.activity import Activity
from .models.age_group import AgeGroup

# Register your models here.
admin.site.register(Activity)
admin.site.register(AgeGroup)