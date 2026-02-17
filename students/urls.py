from django.urls import path
from students import views

urlpatterns = [
    path('signup/', views.signup_page, name="signup"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload, name='upload'),
    path('preview/', views.preview, name="preview"),
    path('preview/manage/', views.preview_manage, name="preview-manage"),
]
