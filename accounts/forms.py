from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        help_text="",
    )
    email = forms.EmailField(
        help_text="",
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        help_text="",
    )
    password2 = forms.CharField(
        label="Password Conformation",
        widget=forms.PasswordInput(),
        help_text="",
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
        ]
