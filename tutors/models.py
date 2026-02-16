from django.db import models
from accounts.models import UserProfile
from students.models import Student

# Create your models here.

class Tutor(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    class_charge = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username} - {self.email} - Tutor"
    
class AcademicRisk(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sgpa_trend = models.FloatField()
    sgpa = models.FloatField()
    name = models.CharField(max_length=200)