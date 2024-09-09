from rest_framework.urls import path

from .views import upload_image, get_zar_rate

urlpatterns = [
    path('fundamentals/upload-image', upload_image, name='upload_image'),
    path('fundamentals/get-zar-rate', get_zar_rate, name='get_zar_rate'),
]
