from django.contrib import admin
from students.models import Student
from accounts.models import UserProfile
from tutors.models import Tutor

# Register your models here.

admin.site.register(Student)
admin.site.register(UserProfile)
admin.site.register(Tutor)