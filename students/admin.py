from django.contrib import admin
from students.models import Student
from students.models import StudentMark
from students.models import Subject
from students.models import SemesterResult

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentMark)
admin.site.register(Subject)
admin.site.register(SemesterResult)