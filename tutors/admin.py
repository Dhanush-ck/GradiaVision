from django.contrib import admin
from tutors.models import Tutor
from tutors.models import AcademicRisk

# Register your models here.

admin.site.register(Tutor)
admin.site.register(AcademicRisk)