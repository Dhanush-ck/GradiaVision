from django.db import models

from students.models import Student

# Create your models here.

class PredictionData(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    prev_sgpa = models.FloatField()
    avg_sgpa = models.FloatField()
    sgpa_trend = models.FloatField()
    avg_marks = models.FloatField()
    avg_difficulty = models.FloatField()
    avg_study_hours = models.FloatField()
    planned_effort = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - Prediction Data"
    
class Prediction(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    predicted_sgpa = models.FloatField()

    def __str__(self):
        return f"{self.student.username} - Prediction"