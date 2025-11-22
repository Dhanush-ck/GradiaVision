from django.shortcuts import render
from django.contrib.auth.models import User

from tutors.forms import TutorForm, TutorSigninForm

from accounts.models import UserProfile
from tutors.models import Tutor

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

            if User.objects.filter(username=email).exists():
                form.add_error('email' ,'Email already exists')
                print("Email already exists")
            else:
                if password != confirm_password:
                    form.add_error('password', "Both passwords should be same")
                    print("Passwords should be same")
                else:
                    user = User(username=email)
                    user.set_password(password)
                    user.save()

                    userProfile = UserProfile.objects.create(
                        user=user,
                        role='tutor'
                    )

                    Tutor.objects.create(
                        profile=userProfile,
                        username=username,
                        email=email,
                        class_charge=class_charge
                    )

                    print("Successfull")

    else:
        form = TutorForm()
    return render(request, 'tutor_signup.html', {
        'form': form,
    })

def signin_page(request):
    if request.method == 'POST':
        form = TutorSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if not Tutor.objects.filter(email=email).exists():
                form.add_error('email', "This email doesn't have any account")
                print("User not found matching email")
            else:
                user = User.objects.get(username=email)
                if not user.check_password(password):
                    form.add_error('password', "Password Error")
                    print("Password Error")
                else:
                    print("Successfull")


    else:
        form = TutorSigninForm()
    return render(request, 'student_signin.html', {
        'form': form,
    })