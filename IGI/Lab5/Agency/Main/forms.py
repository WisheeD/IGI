import re

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import User, Realty, Deal, Review


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'birthdate', 'country', 'city',
                  'phone', 'email', 'password1', 'password2')

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Фамилия'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Имя пользователя'
    }))

    birthdate = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }), label='Дата рождения')

    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Страна'
    }))

    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Город'
    }))

    phone = forms.CharField(
        help_text='Укажите номер телефона в формате +375 (29) XXX-XX-XX',
        widget=forms.TextInput(attrs={'placeholder': '+375 (29) XXX-XX-XX'})
    )

    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Почта'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Подтвердите пароль'
    }))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        phone_pattern = re.compile(r'^\+375 \((25|29|33|44)\) \d{3}-\d{2}-\d{2}$')
        if not phone_pattern.match(phone):
            raise forms.ValidationError('Введите корректный номер телефона в формате +375 (29) XXX-XX-XX')
        return phone

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            today = birthdate.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < 18:
                raise forms.ValidationError('Возраст должен быть 18+')
        return birthdate


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Имя пользователя',
            'id': 'id_username',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Пароль',
            'id': 'id_password',
        })


class RealtyForm(forms.ModelForm):
    class Meta:
        model = Realty
        fields = ('name', 'area', 'address', 'realty_type', 'price', 'description')


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['property', 'client', 'agent', 'deal_type', 'date', 'amount']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'grade']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 5})
        }

        grade = forms.CharField(widget=forms.TextInput(attrs={
            'placeholder': 'Оценка'
        }))

        def clean_grade(self):
            grade = self.cleaned_data.get('grade')
            if grade < 1 or grade > 5:
                raise forms.ValidationError("Оценка должна быть от 1 до 5")
            return grade
