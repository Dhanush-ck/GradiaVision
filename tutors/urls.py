from django.urls import path
from tutors import views

urlpatterns = [
    path('signup', views.signup_page, name='signup'),
]
