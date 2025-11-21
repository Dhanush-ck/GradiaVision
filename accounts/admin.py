from django.contrib import admin
from students.models import Student
from accounts.models import UserProfile

# Register your models here.

admin.site.register(Student)
admin.site.register(UserProfile)