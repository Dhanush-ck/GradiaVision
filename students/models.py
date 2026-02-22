from django.db import models
from accounts.models import UserProfile

import math

# Create your models here.

class Student(models.Model):
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    regno = models.CharField(max_length=20, unique=True)
    semester = models.IntegerField()
    department = models.CharField(max_length=200)
    course = models.CharField(max_length=200)
    current_class = models.CharField(max_length=10, blank=True)

    tutor_email = models.EmailField(max_length=255, default='teacher@gmail.com')

    toughness = models.JSONField(default=dict)
    study_hours = models.JSONField(default=dict)
    sleep_hours = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        self.current_class = self.course + str(math.ceil(self.semester/2))
        super().save(*args, **kwargs)

    def __str__(self):
        # user = self.profile.user
        return f"{self.regno} - Student"
    
class Subject(models.Model):
    course_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    semester = models.IntegerField(default=0)
    credits = models.IntegerField()

    def __str__(self):
        return f"{self.course_code} - {self.semester} - Subject"
    
class SemesterResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    semester = models.IntegerField()
    sgpa = models.FloatField()
    total_credits = models.IntegerField()

    def __str__(self):
        return f"{self.semester} - {self.student.username}"
    
class StudentMark(models.Model):
    ASSESSMENT_CHOICES = [
        ('TH', 'Theory'),
        ('PR', 'Practical'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # semester = models.IntegerField(default=1)
    semester = models.ForeignKey(SemesterResult, on_delete=models.CASCADE)

    assessment_type = models.CharField(
        max_length=2,
        choices=ASSESSMENT_CHOICES
    )

    cca_max = models.IntegerField()
    ese_max = models.IntegerField()
    cca_score = models.IntegerField()
    ese_score = models.IntegerField()
    total_max = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f"{self.subject.course_code} - {self.semester} - {self.assessment_type} - {self.student.username}"

class Notification(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    tutor_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.student.username} - {self.time}"
    