from django.db import models

from students.models import Subject
from students.models import Student

from tutors.models import Tutor

# Create your models here.

class AttendanceSession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)
    semester = models.IntegerField()
    hour = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.date}, Hour - {self.hour}, {self.tutor.username}"
    

class AttendanceRecord(models.Model):
    PRESENT = 'P'
    ABSENT = 'A'
    # LEAVE = 'L'
    # ON_DUTY = 'OD'

    ATTENDANCE_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
        # (LEAVE, 'Leave'),
        # (ON_DUTY, 'On Duty'),
    ]

    attendance_session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=ATTENDANCE_CHOICES, default=ABSENT)

    def __str__(self):
        return f"{self.attendance_session.date}, Hour - {self.attendance_session.hour}, {self.student.username}"