from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from attendance.models import AttendanceSession, AttendanceRecord
from tutors.models import Tutor
from students.models import Student
from students.models import Subject

import json

from students.models import Student

# Create your views here.

def extractStudents(students):
    data = []
    for student in students:
        student_obj = {
            "name": student.username,
            "email": student.email,
            "rollno": int(student.regno[-2:])
        }
        data.append(student_obj)
    return data

def attendance_marking(request):
    user = request.user.userprofile.role

    if user != 'tutor':
        request.session['message'] = "This webpage is only for tutors"
        return redirect('/account/warning')

    user = request.user.userprofile.tutor
    class_charge = user.class_charge

    students = Student.objects.filter(current_class=class_charge).order_by('regno')
    if not students:
        return render(request, 'attendance/attendance_marking.html', {
            'message': "No records",
        })

    course = user.class_charge[:-1]
    year = user.class_charge[-1]

    return render(request, 'attendance/attendance_marking.html', {
        'course': course,
        'year': year,
    })

@csrf_exempt
def get_students(request):

    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    current_class = data['current_class']

    students = Student.objects.filter(current_class=current_class).order_by('regno')

    subject_list = get_subjects(current_class, user)

    if students:
        data = extractStudents(students)
        return JsonResponse({
            'data': data,
            'subjects': subject_list,
        })
    else: 
        return JsonResponse({
            'subjects': subject_list,
        })
    # print(data)

@csrf_exempt
def mark_attendance(request):

    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    # print(data)
    date = data['date']
    hour = data['hour']
    students_attendance = data["attendance"]

    if(AttendanceSession.objects.filter(date=date, hour=hour).exists()):
        return JsonResponse({'message': 'This hours attendance already marked'})

    tutor = Tutor.objects.get(email=user.email)


    for student in students_attendance:
        print(student['email'], student['status'])

    return JsonResponse({'message': "Attendance Updated"})

def get_subjects(class_charge, user):
    
    year = int(class_charge[-1])
    if user.sem == 'E':
        semester = year * 2
    else:
        semester = (year * 2) - 1 

    subjects = Subject.objects.filter(semester=semester, subject_class=class_charge)

    subject_list = []
    for subject in subjects:
        subject_list.append({
            'code': subject.course_code,
            'name': subject.name
        })
    # print(subject_list)

    return subject_list