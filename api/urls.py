# api/urls.py (new file)
from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.predict_image, name='predict_image'),
    path('register/', views.register_user, name='register_user'), 
]