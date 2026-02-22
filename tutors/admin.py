from django.contrib import admin
from tutors.models import Tutor
from tutors.models import AcademicRisk
from tutors.models import AttendanceRisk

# Register your models here.

admin.site.register(Tutor)
admin.site.register(AcademicRisk)
admin.site.register(AttendanceRisk)