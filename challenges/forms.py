from django import forms
from django.forms import inlineformset_factory
from .models import Task, TestCase, Tag


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'slug', 'difficulty', 'tags', 'description', 'starter_code']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Сумма двух чисел'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'sum-two-numbers'}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Подробное описание задачи, форматы входа и выхода, примеры...',
                'style': 'min-height: 220px; line-height: 1.6; font-size: 0.95rem;',
            }),
            'starter_code': forms.Textarea(attrs={
                'class': 'form-control font-monospace',
                'rows': 6,
                'placeholder': 'def solution(a, b):\n    pass',
                'style': 'min-height: 140px; font-size: 0.95rem; tab-size: 4;',
            }),
        }


# Формсет для множественных тест-кейсов
TestCaseFormSet = inlineformset_factory(
    Task,
    TestCase,
    fields=['input_data', 'expected_output'],
    extra=1,  # Количество начальных пустых полей
    can_delete=True,
    widgets={
        'input_data': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Входные данные (например: 5, 10)'}),
        'expected_output': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ожидаемый ответ (например: 15)'}),
    }
)