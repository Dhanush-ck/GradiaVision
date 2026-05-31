from django.shortcuts import render

# Create your views here.

def attendance_marking(request):

    return render(request, 'attendance/attendance_marking.html')