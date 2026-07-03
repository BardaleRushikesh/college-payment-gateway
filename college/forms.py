from django import forms
from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # Only include the fields the student needs to fill out
        fields = ['first_name', 'last_name', 'age', 'email', 'phone', 'department', 'course']

        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'age': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control'}
            ),
            'phone': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'department': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'course': forms.Select(
                attrs={'class': 'form-select'}
            ),
        }