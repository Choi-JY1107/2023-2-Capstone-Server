from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=2)
    password = forms.CharField(min_length=4)
