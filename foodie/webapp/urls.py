from django.urls import path
from .views import upload_photo, dashboard

urlpatterns = [
    path('upload_photo/', upload_photo, name='upload_photo'),
    path('dashboard/', dashboard, name='dashboard'),
]
