from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, FileInput, Select
from django.contrib.auth.models import User
from .models import Course, Quiz
from .models import CustomUser

class CourseInfoForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
              field.widget.attrs.update({'class': 'form-input mt-2 p-2 w-full rounded-md', 'placeholder': f'Enter {field_name}'})

        
class QuizForm(ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'data': FileInput(attrs={
                'class': "px-10 py-20 m-auto bg-white border border-3px ",
                'placeholder': 'Drop'
            }),
             'study_material': FileInput(attrs={
                'class': "px-10 py-20 m-auto bg-white border border-3px ",
                'placeholder': 'Drop'
            })
        }