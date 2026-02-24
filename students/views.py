from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

import json

from students.forms import StudentForm

from students.models import Student
from students.models import StudentMark
from students.models import Subject
from students.models import SemesterResult
from students.models import Notification
from accounts.models import UserProfile
from prediction.models import PredictionData
from prediction.models import Prediction
from tutors.models import AcademicRisk
from tutors.models import Tutor

from students.utils import extract_marklist_data_fyugp
from prediction.predict import predict_score

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

                        current_class = course + str(math.ceil(semester/2))

                        if Tutor.objects.filter(class_charge=current_class).exists():
                            tutor = Tutor.objects.filter(class_charge=current_class).order_by('-updated_at').first()
                            tutor_email = tutor.email
                        else:
                            tutor_email = "teacher@gmail.com"

                        student = Student.objects.create(
                            profile=userProfile,
                            username=username,
                            email=email,
                            regno=regno,
                            semester=semester,
                            department=department,
                            course=course,
                            tutor_email=tutor_email
                        )
                        student.save()

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

    semester = SemesterResult.objects.filter(student=user).count()

    if request.method == "POST":
        # print(pdf_file)

        
            # print(extracted_data)


            ...
    else:
        return render(request, 'students/dashboard.html', {
            'name': user.username,
            'class': current_class,
            'semester': semester,
        })
        

    return render(request, 'students/dashboard.html', {
        'name': user.username,
        'class': current_class,
        'semester': semester,
    })

def upload(request):
    extracted_data = None
    error = None
    user = request.user.userprofile.student

    if request.method == "POST":
        pdf_file = request.FILES.get("pdf")
        extracted_data = extract_marklist_data_fyugp(pdf_file)
        if extracted_data['name'] != user.username.upper():
            error = "Upload only your marklist"
            
            return render(request, 'students/upload.html', {
                'error': error,
            })
        
        if extracted_data['university'] != 'KANNUR UNIVERSITY':
            error = "Upload only your marklist"
            
            return render(request, 'students/upload.html', {
                'error': error,
            })

        course = extracted_data['programme']
        print(course)
        if 'Bachelor of Computer Application' in extracted_data['programme']:
            course = 'BCA'
        if course != user.course:
            error = "Upload only your marklist course"
            
            return render(request, 'students/upload.html', {
                'error': error,
            })

        if SemesterResult.objects.filter(student=user, semester=extracted_data['semester']).exists():
            error = f"Semester {extracted_data['semester']} marklist already uploaded."
            return render(request, 'students/upload.html', {
                'error': error,
            })
        else:
            semester_obj = SemesterResult.objects.create(
                student=user,
                semester=extracted_data['semester'],
                sgpa=extracted_data['sgpa'],
                total_credits=extracted_data['total']['credit']
            )
            for subject in extracted_data['subjects']:
                if not Subject.objects.filter(course_code=subject['code']).exists():
                    subject_obj = Subject.objects.create(
                        course_code=subject['code'],
                        name=subject['name'],
                        semester=extracted_data['semester'],
                        credits=subject['credit']
                    )
                else:
                    subject_obj = Subject.objects.get(course_code=subject['code'])
                StudentMark.objects.create(
                    student=user,
                    subject=subject_obj,
                    semester=semester_obj,
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
                        semester=semester_obj,
                        assessment_type='PR',
                        cca_max=subject['PR']['max']['cca'],
                        ese_max=subject['PR']['max']['ese'],
                        cca_score=subject['PR']['awarded']['cca'],
                        ese_score=subject['PR']['awarded']['ese'],
                        total_max=subject['PR']['max']['cca']+subject['PR']['max']['ese'],
                        total=subject['PR']['awarded']['cca']+subject['PR']['awarded']['ese'],
                    )

            if extracted_data['semester'] != 1:
                student_mark_object = StudentMark.objects.filter(student=user)
                student_marks_percentage = []
                for i in student_mark_object:
                    student_marks_percentage.append((i.total/i.total_max)*100)
                # print(student_marks_percentage)
                average_mark = round(sum(student_marks_percentage)/len(student_marks_percentage), 2)
                # print(average_mark)

                semester_result = SemesterResult.objects.filter(student=user)
                all_sgpa = []
                for sem in semester_result:
                    all_sgpa.append(sem.sgpa)
                average_sgpa = round(sum(all_sgpa)/len(all_sgpa), 2)
                previous_sgpa = all_sgpa[-1]
                sgpa_trend = round(all_sgpa[-2] - all_sgpa[-1], 2)

                predicted_score = predict_score(
                        previous_sgpa,
                        average_sgpa,
                        sgpa_trend,
                        average_mark,
                        3,
                        3,
                        5,
                        )

                if PredictionData.objects.filter(student=user).exists() and Prediction.objects.filter(student=user).exists():
                    prediction_data = Prediction.objects.get(student=user)
                    prediction_data.prev_sgpa = previous_sgpa
                    prediction_data.avg_sgpa = average_sgpa
                    prediction_data.sgpa_trend = sgpa_trend
                    prediction_data.avg_marks = average_mark
                    prediction_data.avg_difficulty = 3
                    prediction_data.avg_study_hours = 3
                    prediction_data.planned_effort = 5
                    prediction_data.save()

                    prediction = Prediction.objects.get(student=user)
                    prediction.predicted_sgpa = predicted_score
                    prediction.save()
                else:

                    PredictionData.objects.create(
                        student=user,
                        prev_sgpa=previous_sgpa,
                        avg_sgpa=average_sgpa,
                        sgpa_trend=sgpa_trend,
                        avg_marks=average_mark,
                        avg_difficulty=3,
                        avg_study_hours=3,
                        planned_effort=5,
                    )

                    Prediction.objects.create(
                        student=user,
                        predicted_sgpa=predicted_score,
                    )

                if sgpa_trend < -0.5 or all_sgpa[-1] < 6.00:
                    AcademicRisk.objects.create(
                        student=user,
                        sgpa_trend=sgpa_trend,
                        sgpa=all_sgpa[-1],
                        name=user.username,
                    )


        success = "File Upload Successfull"
        return render(request, 'students/upload.html', {
            'success': success,
        })

    return render(request, 'students/upload.html', {
        'error': error,
    })

def preview(request):
    user = request.user.userprofile.student
    sem = SemesterResult.objects.filter(student=user)
    current_sem = [i.semester for i in sem]
    return render(request, 'students/preview.html', {
        'current_sem': current_sem,
    })

@csrf_exempt
def preview_manage(request):
    user = request.user.userprofile.student

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        current_semester = data.get("message")
        semester = SemesterResult.objects.get(student=user, semester=current_semester)
        semester_results = StudentMark.objects.filter(student=user, semester=semester)

        subjects = {}

        for index, val in enumerate(semester_results, start=1):
            # print(i.subject.course_code, i.subject.name, i.assessment_type, i.cca_score, i.cca_max, i.ese_score, i.ese_max, i.total, i.total_max)
            subjects[f"Subject{index}"] = {
                'code': val.subject.course_code,
                'name': val.subject.name,
                'type': val.assessment_type,
                'cca_score': val.cca_score,
                'cca_max': val.cca_max,
                'ese_score': val.ese_score,
                'ese_max': val.ese_max,
                'total': val.total,
                'total_max': val.total_max,
                'credits': val.subject.credits
            }

        return JsonResponse({
            "reply": subjects,
        })
    return JsonResponse({"error": "Invalid request"})

@csrf_exempt
def notification_manage(request):
    user = request.user.userprofile.student

    notification_obj = Notification.objects.filter(student=user).order_by('-time')
    notifications = []
    for i in notification_obj:
        temp = {}
        temp['message'] = i.message
        temp['date'] = str(i.time.date())
        hour = f"0{i.time.hour}" if i.time.hour<10 else str(i.time.hour)
        minute = f"0{i.time.minute}" if i.time.minute<10 else str(i.time.minute)
        temp['time'] = f"{hour}:{minute}"
        temp['tutor'] = i.tutor_name
        notifications.append(temp)
    #     print(i.time.date())
    #     print(i.time.hour, i.time.minute)
    
    # print(notifications)

    return JsonResponse({
        'data': notifications,
    })

@csrf_exempt
def graph_manage(request):
    user = request.user.userprofile.student

    data = json.loads(request.body.decode("utf-8"))

    graph_type = data.get('type')
    if graph_type == "sem":
        semester = int(data.get('sem'))
        # print(semester)
        subjects = StudentMark.objects.filter(student=user, semester__semester=semester)
        subjects_total = {}
        for i in subjects:
            subjects_total[i.subject.name] = subjects_total.get(i.subject.name, {})
            subjects_total[i.subject.name]['total'] = subjects_total[i.subject.name].get('total', 0) + i.total
            subjects_total[i.subject.name]['total_max'] = subjects_total[i.subject.name].get('total_max', 0) + i.total_max
        subject_names = []
        subject_percentages = []
        for key, value in subjects_total.items():
            subject_names.append(key)
            percentage = round((value['total']/value['total_max'])*100, 2)
            subject_percentages.append(percentage)
        
        return JsonResponse({
            'subjects': subject_names,
            'percentages': subject_percentages,
        })
    else:
        results = SemesterResult.objects.filter(student=user).order_by('semester')
        semesters = []
        scores = []
        for result in results:
            semesters.append(f"Semester {result.semester}")
            scores.append(result.sgpa)
        if Prediction.objects.filter(student=user).exists():
            prediction = Prediction.objects.get(student=user)
            semesters.append(f"Semester {len(results)+1}")
            scores.append(prediction.predicted_sgpa)
        return JsonResponse({
            'semesters': semesters,
            'scores': scores,
        })