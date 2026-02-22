from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from tutors.forms import TutorForm

from accounts.models import UserProfile
from tutors.models import Tutor
from students.models import Student
from students.models import Notification
from tutors.models import AttendanceRisk
from tutors.models import AcademicRisk

import json

from tutors.attendance_extraction_manager import extract_attendace_data

# Create your views here.

def signup_page(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            class_charge = form.cleaned_data['class_charge']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirmPassword')
            security_question =  form.cleaned_data['security_question']
            security_answer = form.cleaned_data['security_answer']

            if User.objects.filter(username=email).exists():
                form.add_error('email' ,'Email already exists')
                print("Email already exists")
            else:
                if password != confirm_password:
                    form.add_error('password', "Both passwords should be same")
                    print("Passwords should be same")
                else:
                    user = User(username=email, email=email)
                    user.set_password(password)
                    user.save()

                    userProfile = UserProfile.objects.create(
                        user=user,
                        role='tutor',
                        security_question=security_question,
                    )
                    userProfile.security_answer = make_password(security_answer)
                    userProfile.save()

                    Tutor.objects.create(
                        profile=userProfile,
                        username=username,
                        email=email,
                        class_charge=class_charge
                    )

                    print("Successfull")
                    return redirect('/account/signin')

    else:
        form = TutorForm()
    return render(request, 'tutors/signup.html', {
        'form': form,
    })

def dashboard(request):

    user = request.user.userprofile.tutor

    return render(request, 'tutors/dashboard.html', {
        'name': user.username, 
        'class_charge': user.class_charge,
    })

def upload(request):

    user = request.user.userprofile.tutor

    if request.method == "POST":
        pdf_file = request.FILES.get("pdf")
        regno_count = int(request.POST.get('regno'))
        attendance_count = int(request.POST.get('attendance'))
        semester = int(request.POST.get('semester'))
        extracted_data = extract_attendace_data(regno_count, attendance_count, pdf_file)

        for data in extracted_data:
            # print(data['regno'], data['attendance'])
            if Student.objects.filter(regno=data['regno']).exists():
                student = Student.objects.get(regno=data['regno'])
                # print(student.username)
                # print(semester)

                Notification.objects.create(
                    student=student,
                    message=f"Your semester {semester} attendance is {data['attendance']}%",
                    tutor_name=user.username
                )

                if data['attendance'] < 75:
                    AttendanceRisk.objects.create(
                        student=student,
                        attendance=data['attendance']
                    )

        return render(request, 'tutors/upload.html')
    return render(request, 'tutors/upload.html')

@csrf_exempt
def risk(request):
    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    risk_type = data.get('message')

    if risk_type == "attendance":
        # print('attendance')
        alert = AttendanceRisk.objects.filter(student__tutor_email=user.email)
        alerts = []
        for i in alert:
            temp = {}
            temp['attendance'] = i.attendance
            temp['name'] = i.student.username
            temp['regno'] = i.student.regno
            alerts.append(temp)
        
        return JsonResponse({'attendance': alerts})


    else:
        # print('academic')
        alert = AcademicRisk.objects.filter(student__tutor_email=user.email)
        alerts = []
        for i in alert:
            temp = {}
            temp['sgpa_trend'] = i.sgpa_trend
            temp['sgpa'] = i.sgpa
            temp['name'] = i.name
            temp['regno'] = i.student.regno
            alerts.append(temp)

        return JsonResponse({'academic': alerts})

@csrf_exempt    
def update_class(request):
    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    class_charge = data.get('message')
    # print(class_charge)

    Student.objects.filter(current_class=class_charge).update(tutor_email=user.email)
    # students = Student.objects.all()

    return JsonResponse({'message': 'Updated Success'})