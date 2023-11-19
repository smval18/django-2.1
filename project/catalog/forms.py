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



class NewApplicationForm(forms.ModelForm):

    class Meta:
        model = models.Application
        fields = (
            'name',
            'description',
            'image',
            'category'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(NewApplicationForm, self).__init__(*args, **kwargs)

    def clean_image(self):
        img = self.cleaned_data.get('image')

        if not img:
            raise forms.ValidationError("ДОБАВЬТЕ ИЗОБРАЖЕНИЕ")

        if img.size > 2*1024*1024:
            raise forms.ValidationError("ИЗОБРАЖЕНИЕ БОЛЬШОЕ, ДОБАВЬТЕ МЕНЬШЕ")

        return img

    def save(self, commit=True) -> Any:
        app = super(NewApplicationForm, self).save(commit=False)

        app.user = self.user
        app.status = models.Status.get_by_name('новая')

        if commit:
            app.save()

        return app


class ApplicaionForm(forms.ModelForm):
    class Meta:
        model = models.Application
        fields = (
            'description',
            'image',
            'status'
        )

    def __init__(self, *args, **kwargs) -> None:
        id = kwargs.pop('record_id', None)

        super().__init__(*args, **kwargs)

        model = models.Application.objects.get(pk=id)

        if model.status.name != 'New':
            del self.fields['status']

            return

        statuses = models.Status.objects.exclude(pk=model.status.pk).all()

        self.fields['status'].choices = ((s.pk, s.name) for s in statuses)

    def clean_image(self):
        img = self.cleaned_data.get('image')

        if not img:
            raise forms.ValidationError("ДОБАВЬТЕ ИЗОБРАЖЕНИЕ")

        if img.size > 2 * 1024 * 1024:
            raise forms.ValidationError("ИЗОБРАЖЕНИЕ БОЛЬШОЕ, ДОБАВЬТЕ МЕНЬШЕ")

        return img

    def save(self, commit=True) -> Any:
        app = super(ApplicaionForm, self).save(commit=False)
        app.image = self.cleaned_data.get('image')


        if commit:
            app.save()

        return app

class CategoryForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = (
            'name',
        )

