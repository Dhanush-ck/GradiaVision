from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from students.forms import StudentForm

from students.models import Student
from students.models import StudentMark
from students.models import Subject
from students.models import SemesterResult
from accounts.models import UserProfile

from students.utils import extract_marklist_data_fyugp

import math

# Create your views here.

def signup_page(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            email = form.cleaned_data['email'].strip()
            regno = form.cleaned_data['regno'].strip()
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

    if request.method == "POST":
        # print(pdf_file)

        
            # print(extracted_data)


            ...
    else:
        return render(request, 'students/dashboard.html', {
            'name': user.username,
            'class': current_class,
        })
        

    return render(request, 'students/dashboard.html', {
        'name': user.username,
        'class': current_class,
    })

def upload(request):
    extracted_data = None
    error = None
    user = request.user.userprofile.student

    if request.method == "POST":
        pdf_file = request.FILES.get("pdf")
        extracted_data = extract_marklist_data_fyugp(pdf_file)
        if extracted_data['name'] != user.username.upper():
            error = "Upload your marklist"
            
            return render(request, 'students/upload.html', {
                'error': error,
            })
        else:
            for subject in extracted_data['subjects']:
                if not Subject.objects.filter(course_code=subject['code']).exists():
                    subject_obj = Subject.objects.create(
                        course_code=subject['code'],
                        name=subject['name'],
                        credits=subject['credit']
                    )
                else:
                    subject_obj = Subject.objects.get(course_code=subject['code'])
                StudentMark.objects.create(
                    student=user,
                    subject=subject_obj,
                    semester=extracted_data['semester'],
                    assessment_type='TH',
                    cca_max=subject['TH']['max']['cca'],
                    ese_max=subject['TH']['max']['ese'],
                    cca_score=subject['TH']['awarded']['cca'],
                    ese_score=subject['TH']['awarded']['ese'],
                    total_max=subject['TH']['max']['cca']+subject['TH']['max']['ese'],
                    total=subject['TH']['awarded']['cca']+subject['TH']['awarded']['ese'],
                )
                if 'PR' in subject:
                    StudentMark.objects.create(
                        student=user,
                        subject=subject_obj,
                        semester=extracted_data['semester'],
                        assessment_type='PR',
                        cca_max=subject['PR']['max']['cca'],
                        ese_max=subject['PR']['max']['ese'],
                        cca_score=subject['PR']['awarded']['cca'],
                        ese_score=subject['PR']['awarded']['ese'],
                        total_max=subject['PR']['max']['cca']+subject['PR']['max']['ese'],
                        total=subject['PR']['awarded']['cca']+subject['PR']['awarded']['ese'],
                    )

            SemesterResult.objects.create(
                student=user,
                semester=extracted_data['semester'],
                sgpa=extracted_data['sgpa'],
                total_credits=extracted_data['total']['credit']
            )
            success = "File Upload Successfull"
        return render(request, 'students/upload.html', {
            'success': success,
        })

    return render(request, 'students/upload.html', {
        'error': error,
    })

     