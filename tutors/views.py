from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from tutors.forms import TutorForm

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
