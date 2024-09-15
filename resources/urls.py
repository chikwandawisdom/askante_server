from rest_framework.urls import path

from .views import ResourceList, ResourceDetail

urlpatterns = [
    path('resources', ResourceList.as_view(), name='resource-list'),
    path('resources/<int:pk>', ResourceDetail.as_view(), name='resource-detail'),
]
