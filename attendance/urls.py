from django.urls import path
from attendance import views

urlpatterns = [
    path('mark/', views.attendance_marking, name='attendance_marking')
]
