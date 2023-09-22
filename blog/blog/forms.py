from django import forms
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, FileInput, Select
from django.contrib.auth.models import User
from .models import Comment, Post
from .models import CustomUser

class BlogForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
