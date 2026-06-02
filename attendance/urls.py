from django.urls import path
from attendance import views

urlpatterns = [
    path('mark/', views.attendance_marking, name='attendance_marking'),
    path('getStudents/', views.get_students, name="get_students"),
    path('markAttendance/', views.mark_attendance, name="mark_attendance"),
]
