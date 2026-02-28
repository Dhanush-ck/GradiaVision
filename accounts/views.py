from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm

from accounts.forms import SigninForm, EmailForm

# # Create your views here.

def select_role(request):
    if request.method == 'POST':
            role = request.POST.get('role')

            if role == 'student':
                print("student")
                return redirect('/student/signup')
            elif role == 'tutor':
                print("tutor")
                return redirect('/tutor/signup')

    return render(request, 'accounts/role.html')

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            # email = request.POST['email']
            # password = request.POST['password']

            email = form.cleaned_data['email'].lower().strip()
            password = form.cleaned_data['password'].strip()

            try:
                user_obj = User.objects.get(username=email)
            except User.DoesNotExist:
                user_obj = None
                
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                print("Login successfull")
                if user.userprofile.role == 'student':
                    print("Redirecting to student dashboard")
                    return redirect('student_dashboard')
                else:
                    print("Redirecting to tutor dashboard")
                    return redirect('tutor_dashboard')

            if user_obj is  None:
                error = "Invalid password or email"
                print('Invalid password or email')
            else:
                error = "Incorrect password. Try again. "
                print('Incorrect password. Try again.')

        return render(request, 'accounts/signin.html', {
            'error': error,
            'form': form,
        })

    else:
        form = SigninForm()

    
    return render(request, 'accounts/signin.html', {
        'form': form
    })

def verify_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if not User.objects.filter(username=email).exists():
                print("Email doesn't exist")
                error = "Email doesn't exist"
                return render(request, 'accounts/reset_email.html', {
                    'form': form,
                    'error': error,
                })
            else:
                request.session['email'] = email
                return redirect('question_view')

    else:
        form = EmailForm()
    return render(request, 'accounts/verify_email.html', {
        'form': form,
    })

def question_view(request):
    email = request.session.get('email')
    user = User.objects.get(username=email)

    if request.method == 'POST':
        answer = request.POST['answer']

        if not check_password(answer, user.userprofile.security_answer):
            print("Invalid answer")
            return render(request, 'accounts/question_view.html', {
                'question': user.userprofile.security_question,
                'error': "Invalid answer",
            })
        
        print('Password Reset Redirect')

        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='accounts/password_reset_email.html',
                subject_template_name='accounts/password_reset_subject.txt',
            )

            return redirect('/account/reset/done')

    return render(request, 'accounts/question_view.html', {
        'question': user.userprofile.security_question,
    })

def signout(request):
    logout(request)
    print("Logout")
    return redirect('/account/signin/')