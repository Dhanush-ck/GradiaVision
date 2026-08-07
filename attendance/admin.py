from django.contrib import admin
from attendance.models import AttendanceRecord, AttendanceSession

# Register your models here.

admin.site.register(AttendanceRecord)
admin.site.register(AttendanceSession)