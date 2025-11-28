from django import forms

class SigninForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'id': 'email'}))
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'id': 'password'}))

class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Enter your email', 'id': 'email'}))