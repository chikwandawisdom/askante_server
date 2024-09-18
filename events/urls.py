from rest_framework.urls import path

from .views import ActivityList, ActivityDetail, AgeGroupList, AgeGroupDetails
from .views import (add_students_to_age_group, get_students_in_age_group, remove_student_from_age_group, add_activity_period,
                    update_activity_period, get_activity_periods_of_a_class, delete_activity_period,
                    AgeGroupActivityList, AgeGroupActivityDetails)


urlpatterns = [
    path('activities', ActivityList.as_view(), name='activity-list'),
    path('activities/<int:pk>', ActivityDetail.as_view(), name='activity-detail'),
    path('age-groups', AgeGroupList.as_view(), name='age-groups-list'),
    path('age-groups/<int:pk>', AgeGroupDetails.as_view(), name='age-groups-detail'),
    path('age-groups/add-students', add_students_to_age_group, name='add-students-to-age-group'),
    path('age-groups/students', get_students_in_age_group, name='get-students-in-age-group'),
    path('age-groups/remove-student', remove_student_from_age_group, name='remove-student-from-age-group'),
    path('age-groups/activities', AgeGroupActivityList.as_view(), name='age-group-activities'),
    path('age-groups/activities/<int:pk>', AgeGroupActivityDetails.as_view(), name='age-group-subject'),
    path('age-groups/add-students', add_students_to_age_group, name='add-students-to-age-group'),
    path('age-groups/students', get_students_in_age_group, name='get-students-in-age-group'),
    path('age-groups/remove-student', remove_student_from_age_group, name='remove-student-from-age-group'),
    path('add-activity-period', add_activity_period, name='add-activity-period'),
    path('update-activity-period/<int:pk>', update_activity_period, name='update-activity-period'),
    path('get-activity-periods', get_activity_periods_of_a_class, name='get-activity-periods'),
    path('delete-activity-period/<int:pk>', delete_activity_period, name='delete-activity-period'),
]
				
