from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from students.forms import StudentForm

from students.models import Student
from accounts.models import UserProfile

from students.utils import extract_marklist_data

import math

# Create your views here.

def signup_page(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            regno = form.cleaned_data['regno']
            semester = form.cleaned_data['semester']
            department = request.POST.get('department')
            course = request.POST.get('course')
            # password = request.POST.get('password')
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirmPassword')
            security_question =  form.cleaned_data['security_question']
            security_answer = form.cleaned_data['security_answer']

            # print(f"username: {username}")
            # print(f"email: {email}")
            # print(f"regno = {regno}")
            # print(f"semester = {semester}")
            # print(f"department = {department}")
            # print(f"course = {course}")
            # print(f"Password = {password}")
            # print(f"Confirmed Password = {confirm_password}")

            if Student.objects.filter(regno=regno).exists():
                form.add_error('regno', "Registration no already exist")
                print("Registration no already exist")
            else:
                if User.objects.filter(username=email).exists():
                    form.add_error('email', 'Email already exists')
                    print('student already exists')
                else:
                    if password != confirm_password:
                        form.add_error('password', "Both passwords should be same")
                        print("password error")
                    else:
                        user = User(username=email, email=email)
                        user.set_password(password)
                        user.save()

                        userProfile = UserProfile.objects.create(
                            user=user,
                            role='student',
                            security_question=security_question,
                        )
                        userProfile.security_answer = make_password(security_answer)
                        userProfile.save()

                        Student.objects.create(
                            profile=userProfile,
                            username=username,
                            email=email,
                            regno=regno,
                            semester=semester,
                            department=department,
                            course=course,
                        )

                        print("Successfull")
                        return redirect('/account/signin')
   
    else: 
        form = StudentForm()
    return render(request, 'students/signup.html', {
        'form': form,
    })

def dashboard(request):
    user = request.user.userprofile.student
    current_class = user.course + str(math.ceil(user.semester/2))

    return render(request, 'students/dashboard.html', {
        'name': user.username,
        'class': current_class,
    })

def pdf_extract(request):
    ...