from django.shortcuts import render, redirect

from students.models import Student

# Create your views here.

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
            'message': "No records"
        })
        
    data = []
    for student in students:
        student_obj = {
            "name": student.username,
            "email": student.email,
            "rollno": int(student.regno[-2:])
        }
        data.append(student_obj)
        # print(student_obj)

    return render(request, 'attendance/attendance_marking.html', {
        'data': data,
    })