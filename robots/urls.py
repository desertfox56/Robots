# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/robot/', views.robot_endpoint, name='robot_endpoint'),
    path('download/', views.generate_excel, name='generate_excel'),
]