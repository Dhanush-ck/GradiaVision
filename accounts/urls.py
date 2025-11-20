from django.urls import path 
from accounts import views

urlpatterns = [
    path('role', views.select_role, name='role')
]
