from django import forms

class registerForm(forms.Form):
    name = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=20)
    phone = forms.IntegerField()
    role = forms.CharField(max_length=20)
    username = forms.CharField(max_length=20)
    password = forms.PasswordInput()