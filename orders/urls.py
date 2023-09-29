from django.urls import path
from . import views

urlpatterns = [
    path('api/robot/', views.order_robot_endpoint, name='order_robot_endpoint'),
    path('api/robot/appear/', views.robot_appear, name='robot_appear'),
]