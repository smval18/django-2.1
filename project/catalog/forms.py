from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList

from . import models


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(),
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[а-яА-ЯёЁ -]*$',
                message='ТОЛЬКО КИРИЛЛИЦА',
            ),
        ],
    )
    middle_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(),
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[а-яА-ЯёЁ -]*$',
                message='ТОЛЬКО КИРИЛЛИЦА',
            ),
        ],
    )
    last_name = forms.CharField(
        label='Отчество',
        widget=forms.TextInput(),
        required=True,
        validators=[
            validators.RegexValidator(
                regex=r'^[а-яА-ЯёЁ -]*$',
                message='ТОЛЬКО КИРИЛЛИЦА',
            ),
        ],
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(),
        required=True,
    )
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(),
        required=True,
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
        required=True,
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(),
        required=True,
    )
    tos = forms.BooleanField(
        label='Я ознакомлен и согласен с правилами пользования',
        widget=forms.CheckboxInput(),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
            'tos',
        )

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 == '' or password2 == '':
            raise forms.ValidationError('ЗАПОЛИНИТЕ ПАРОЛЬ')

        if password1 != password2:
            raise forms.ValidationError('ПАРОЛИ НЕ СОВПАДАЮТ')

        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)

        if commit:
            user.save()

        return user
