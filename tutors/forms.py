from django import forms

class TutorForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your name', 'id': 'username'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'id': 'email'}))
    class_charge = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter the class in charge', 'id': 'class-charge'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'id': 'password'}))

class TutorSigninForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Enter your email", 'id':'email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password' ,'id':'password'}))
