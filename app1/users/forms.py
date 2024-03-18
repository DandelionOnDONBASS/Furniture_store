from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordResetForm

from .models import User


class UserLoginForm(AuthenticationForm):

    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "autofocus": True,
    #             "class": "form-control",
    #             "placeholder": "Введите ваше имя пользователя",
    #         }
    #     )
    # )
    # password = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "autocomplete": "current-password",
    #             "class": "form-control",
    #             "placeholder": "Введите ваш пароль",
    #         }
    #     ),
    # )

    class Meta:
        model = User
        fields = ["username", "password"]



class UserRegistrationForm(UserCreationForm):

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    class Meta:
        model = User
        fields = ("first_name", "last_name","username", "email", "password1", "password2")



class UserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("image","first_name", "last_name","username", "email")


