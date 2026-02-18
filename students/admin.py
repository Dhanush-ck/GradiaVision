from django.contrib import admin
from students.models import Student
from students.models import StudentMark
from students.models import Subject
from students.models import SemesterResult
from students.models import Notification

# Register your models here.

admin.site.register(Student)
admin.site.register(StudentMark)
admin.site.register(Subject)
admin.site.register(SemesterResult)
# admin.site.register(Notification)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('student', 'message', 'time', 'tutor_name')
    readonly_fields = ('time',)
