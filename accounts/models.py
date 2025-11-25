from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    # username = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10,  choices=[
        ("student", "Student"),
        ("tutor", "Tutor"),
        ("admin", "Admin")
                          ])
    
    security_question = models.CharField(max_length=100, blank=True)
    security_answer = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"
    