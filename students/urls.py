from django.urls import path
from students import views

urlpatterns = [
    path('signup', views.signup_page, name="signup"),
    path('dashboard', views.dashboard, name='dashboard'),
]
