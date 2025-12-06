from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")


class RegisterFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2', 'role', 'image',
                  'mailing', 'mailing_frequency']


class ResetRequestFrom(forms.Form):
    email = forms.EmailField()


class ResetConfirmFrom(forms.Form):
    uid = forms.CharField(label='uid из письма')
    token = forms.CharField(label='token из письма')
