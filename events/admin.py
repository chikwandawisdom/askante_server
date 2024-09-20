from django.contrib import admin

from .models.activity import Activity
from .models.age_group import AgeGroup
from .models.activity_timetables import ActivityPeriod
from .models.age_group_activity import AgeGroupActivity
from .models.event import Event

# Register your models here.
admin.site.register(Activity)
admin.site.register(AgeGroup)
admin.site.register(ActivityPeriod)
admin.site.register(AgeGroupActivity)
admin.site.register(Event)