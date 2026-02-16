from django.urls import path
from chatbot import views

urlpatterns = [
    path("dashboard/", views.chatbot, name='chatbot_dashboard'),
    path("reply/", views.reply, name='reply')
]
