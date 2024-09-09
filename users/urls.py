from rest_framework.urls import path

from users.views import login, authenticate, register, get_all_users, change_user_active_status, forgot_password, reset_password

urlpatterns = [
    path('users/login', login, name='login'),
    path('users/authenticate', authenticate, name='authenticate'),
    path('users/register', register, name='register'),
    path('admin/users', get_all_users, name='get_all_users'),
    path('admin/users/<int:pk>', change_user_active_status, name='change_user_active_status'),
    path('users/forgot-password', forgot_password, name='forgot_password'),
    path('users/reset-password', reset_password, name='reset_password'),
]
