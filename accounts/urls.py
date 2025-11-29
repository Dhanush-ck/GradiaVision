from django.urls import path 
from accounts import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('role/', views.select_role, name='role'),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html"
        ),
        name="password_reset_done",
    ),

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url="account/reset/complete",  
        ),
        name="password_reset_confirm",
    ),

    path(
        "reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path('signin/', views.signin, name='signin'),
    path('verify/email/', views.verify_email, name='verify_email'),
    path('question/', views.question_view, name='question_view'),
    path('signout/', views.signout, name='signout'),
]
