"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('institutions.urls')),
    path('api/', include('employees.urls')),
    path('api/', include('fundamentals.urls')),
    path('api/', include('students.urls')),
    path('api/', include('registry.urls')),
    path('api/', include('academic.urls')),
    path('api/', include('library.urls')),
    path('api/', include('finance.urls')),
    path('api/', include('reports.urls')),
    path('api/', include('book_shop.urls')),
    path('api/', include('resources.urls')),
    path('api/', include('events.urls')),
]
