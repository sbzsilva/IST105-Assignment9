from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authenticate/', views.authenticate_view, name='authenticate'),
    path('devices/', views.list_devices_view, name='list_devices'),
    path('interfaces/', views.device_interfaces_view, name='device_interfaces'),
    path('logs/', views.view_logs, name='view_logs'),
]