from django import forms

class StudentForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your name', 'id': 'username'}) )
    regno = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter your registration no', 'id': 'regno'}))
    semester = forms.IntegerField(min_value=1, max_value=8, widget=forms.TextInput(attrs={'placeholder': 'Enter your semester', 'id': 'semester'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password' ,'id':'password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':"Enter your email", 'id':'email'}))