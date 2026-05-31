from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from tutors.forms import TutorForm

from accounts.models import UserProfile
from tutors.models import Tutor
from students.models import Student
from students.models import StudentMark
from students.models import Notification
from students.models import SemesterResult
from tutors.models import AttendanceRisk
from tutors.models import AcademicRisk

import json

from tutors.attendance_extraction_manager import extract_attendace_data

# Create your views here.

def signup_page(request):
    if request.method == 'POST':
        form = TutorForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].strip()
            email = form.cleaned_data['email'].lower().strip()
            class_charge = form.cleaned_data['class_charge']
            password = form.cleaned_data['password'].strip()
            confirm_password = request.POST.get('confirmPassword').strip()
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

@login_required(login_url='signin')
def dashboard(request):

    user = request.user.userprofile.role

    if user != "tutor":
        request.session['message'] = "This webpage is only for tutors"
        return redirect('/account/warning')

    user = request.user.userprofile.tutor

    return render(request, 'tutors/dashboard.html', {
        'name': user.username, 
        'class_charge': user.class_charge,
    })

@login_required(login_url='signin')
def upload(request):

    user = request.user.userprofile.role

    if user != "tutor":
        request.session['message'] = "This webpage is only for tutors"
        return redirect('/account/warning')

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

        return render(request, 'tutors/upload.html', {
            'success': 'Upload done',
        })
    return render(request, 'tutors/upload.html')

@csrf_exempt
def risk(request):
    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    risk_type = data.get('message')

    if risk_type == "attendance":
        # print('attendance')
        alert = AttendanceRisk.objects.filter(student__current_class=user.class_charge)
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
        alert = AcademicRisk.objects.filter(student__current_class=user.class_charge).order_by('sgpa_trend')
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
    user.class_charge = class_charge
    user.save()
    # students = Student.objects.all()

    return JsonResponse({'message': 'Updated Success'})

@csrf_exempt 
def tutor_graph(request):

    user = request.user.userprofile.tutor

    grades_count = {
        'O': 0,
        'A+': 0,
        'A': 0,
        'B+': 0,
        'B': 0,
        'C': 0,
        'P': 0,
        'F': 0,
    }

    students = Student.objects.filter(current_class=user.class_charge)

    for student in students:
        sgpas = []
        semesters = SemesterResult.objects.filter(student__current_class=student.current_class)
        if(semesters):
            for semester in semesters:
                sgpas.append(semester.sgpa)
            sgpa = sum(sgpas)/len(sgpas)

            if sgpa >= 9.5:
                grades_count['O'] += 1
            elif sgpa >= 8.5:
                grades_count['A+'] += 1
            elif sgpa >= 7.5:
                grades_count['A'] += 1
            elif sgpa >= 6.5:
                grades_count['B+'] += 1
            elif sgpa >= 5.5:
                grades_count['B'] += 1
            elif sgpa >= 4.5:
                grades_count['C'] += 1
            elif sgpa >= 3.5:
                grades_count['P'] += 1
            else:
                grades_count['F'] += 1

    # print(list(grades_count.values()))            
    # print(list(grades_count.keys()))            

    return JsonResponse({
        'count': list(grades_count.values()),
        'grades': list(grades_count.keys()),
    })

@csrf_exempt
def add_notification(request):
    user = request.user.userprofile.tutor

    data = json.loads(request.body.decode("utf-8"))

    message = data.get('message')

    students = Student.objects.filter(current_class=user.class_charge)

    for student in students:
        Notification.objects.create(
            student=student,
            message=message,
            tutor_name=user.username,
        )

    return JsonResponse({'message': 'Notification added successfully'})

@login_required(login_url='signin')
def view_student(request):
    
    user = request.user.userprofile.role

    if user != "tutor":
        request.session['message'] = "This webpage is only for tutors"
        return redirect('/account/warning')

    user = request.user.userprofile.tutor

    students = Student.objects.filter(current_class=user.class_charge).order_by('regno')

    data = []
    for student in students:
        student_obj = {
            "name": student.username,
            "email": student.email,
            "regno": student.regno,
        }
        data.append(student_obj)
    
    course = user.class_charge[:-1]
    year = user.class_charge[-1]

    return render(request, 'tutors/view_students.html', {
        'data': data, 
        'course': course,
        'year': year,
    })

@csrf_exempt
def filter_student(request):

    data = json.loads(request.body.decode("utf-8"))

    class_info = data.get('message')

    students = Student.objects.filter(current_class=class_info).order_by('regno')

    student_data = []
    for student in students:
        student_obj = {
            "name": student.username,
            "email": student.email,
            "regno": student.regno,
        }
        student_data.append(student_obj)

    return JsonResponse({
        'class_info': student_data
    })

@csrf_exempt
def student_card(request):

    data = json.loads(request.body.decode("utf-8"))

    email = data.get('email')

    student = Student.objects.get(email=email)

    semesters_data = SemesterResult.objects.filter(student=student).order_by('semester')
    semesters = []
    for semester in semesters_data:
        semesters.append(semester.semester)


    graph_data = update_student_card_graph(student, "course")

    return JsonResponse({
        'name': student.username,
        'email': student.email,
        'regno': student.regno,
        'semester': student.semester,
        'aadhaar': student.aadhaar[:4] + " " + student.aadhaar[4:8] + " " + student.aadhaar[8:],
        'semesters': graph_data['semesters'],
        'scores': graph_data['scores'],
        'semester_count': semesters,
    })


def update_student_card_graph(user, graph_type, semester=1):
    if graph_type == "sem":
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
        
        graph_data = {
            'subjects': subject_names,
            'percentages': subject_percentages,
        }

        return graph_data
    else:
        results = SemesterResult.objects.filter(student=user).order_by('semester')
        semester_numbers = []
        semesters = []
        scores = []
        for result in results:
            semesters.append(f"Semester {result.semester}")
            semester_numbers.append(result.semester)
            scores.append(result.sgpa)
        # if Prediction.objects.filter(student=user).exists():
        #     prediction = Prediction.objects.get(student=user)
        #     semesters.append(f"Semester {max(semester_numbers)+1} (Predicted)")
        #     scores.append(prediction.predicted_sgpa)
        graph_data = {
            'semesters': semesters,
            'scores': scores,
        }

        return graph_data
    
@csrf_exempt
def handle_graph_type(request):

    data = json.loads(request.body.decode("utf-8"))

    email = data.get('email')
    graph_type = data.get('graph_type')
    semester = data.get('semester')

    student = Student.objects.get(email=email)
    graph_data  = update_student_card_graph(student, graph_type, semester)

    if graph_type == "course":    
        return JsonResponse({
            "semesters": graph_data['semesters'],
            "scores": graph_data['scores'],
        })
    else:
        print(graph_data)
        return JsonResponse({
            "subjects": graph_data['subjects'],
            'percentages': graph_data['percentages'],
        })