from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Classroom

class CustomRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProfileRoleForm(forms.ModelForm):
    """Форма смены роли"""
    class Meta:
        model = Profile
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-select'})
        }


class CreateClassForm(forms.ModelForm):
    """Форма создания класса (для Учителя)"""
    class Meta:
        model = Classroom
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Python 10-А класс'})
        }


class JoinClassForm(forms.Form):
    """Форма ввода кода (для Ученика)"""
    code = forms.CharField(
        max_length=10,
        label="Код класса",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите 6-значный код (например: X8K2P9)'})
    )