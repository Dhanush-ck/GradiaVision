from django.urls import path
from tutors import views

urlpatterns = [
    path('signup/', views.signup_page, name='signup'),
    path('dashboard/', views.dashboard, name='tutor_dashboard'),
    path('attendance/', views.upload, name='attendance'),
    path('risk/', views.risk, name='risk'),
    path('update/class/', views.update_class, name='update-class'),
    path('graph/', views.tutor_graph, name='tutor_graph'),
    path('notification/add/', views.add_notification, name="add_notification"),
    path('students/', views.view_student, name='view_students'),
    path('filter/', views.filter_student, name="filter_name"),
    path('studentCard/', views.student_card, name="student_card"),
    path('graphType/', views.handle_graph_type, name="handle_graph_type"),
]
