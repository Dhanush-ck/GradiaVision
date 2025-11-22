from django.db import models
from accounts.models import UserProfile

# Create your models here.

class Student(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    regno = models.CharField(max_length=20)
    semester = models.IntegerField()
    department = models.CharField(max_length=200)
    course = models.CharField(max_length=200)

    toughness = models.JSONField(default=dict)
    study_hours = models.JSONField(default=dict)
    sleep_hours = models.JSONField(default=dict)

    def __str__(self):
        # user = self.profile.user
        return f"{self.regno} - Student"