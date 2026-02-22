from django.urls import path
from tutors import views

urlpatterns = [
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard, name='tutor_dashboard'),
    path('attendance/', views.upload, name='attendance'),
    path('risk/', views.risk, name='risk'),
    path('update/class/', views.update_class, name='update-class'),
]
