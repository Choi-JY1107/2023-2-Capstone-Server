from django import forms
from django.core.exceptions import ValidationError
from users.models import User


# Form is only used for template to develop
class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=2,
        widget=forms.TextInput(
            attrs={"placeholder": "사용자명 (2자리 이상)"},
        ),
    )
    password = forms.CharField(
        min_length=4,
        widget=forms.PasswordInput(
            attrs={"placeholder": "비밀번호 (4자리 이상)"},
        )
    )


class SignupForm(forms.Form):
    username = forms.CharField()
    nickname = forms.CharField()
    phone_number = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
