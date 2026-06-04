from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


from attendance.models import AttendanceSession, AttendanceRecord
from tutors.models import Tutor
from students.models import Student
from students.models import Subject

import json
from datetime import datetime

from students.models import Student

# Create your views here.

def extractStudents(students):
    data = []
    for student in students:
        student_obj = {
            "name": student.username,
            "regno": student.regno,
            "rollno": int(student.regno[-2:])
        }
        data.append(student_obj)
    return data

@login_required(login_url='signin')
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

    year = int(user.class_charge[-1])
    semester = (year*2) if (user.sem == 'E') else (year*2) - 1

    date_raw = data['date']
    date = datetime.strptime(date_raw, "%Y-%m-%d").date()
    hour = data['hour']
    students_attendance = data["attendance"]
    subject_code = data['subject']
    current_class = data['current_class']

    if(AttendanceSession.objects.filter(date=date, hour=hour).exists()):
        return JsonResponse({'message': 'This hours attendance already marked'})
    else :
        tutor = Tutor.objects.get(email=user.email)
        subject = Subject.objects.get(course_code=subject_code)

        attendance_session = AttendanceSession.objects.create(
            subject=subject,
            tutor=tutor,
            semester=semester,
            hour=hour,
            date=date,
        )

        present_regnos = [student['regno'] for student in students_attendance if student['status'] == 'P']
        absent_regnos = [student['regno'] for student in students_attendance if student['status'] == 'A']

        present_students = Student.objects.filter(regno__in=present_regnos)
        absent_students = Student.objects.filter(regno__in=absent_regnos)

        for student in present_students:
            AttendanceRecord.objects.create(
                attendance_session=attendance_session,
                student=student,
                status=AttendanceRecord.PRESENT
            )

        for student in absent_students:
            AttendanceRecord.objects.create(
                attendance_session=attendance_session,
                student=student,
                status=AttendanceRecord.ABSENT
            )
        
    # for student in students_attendance:
    #     print(student['regno'], student['status'])

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