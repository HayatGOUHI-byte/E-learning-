from django import forms

from blog.models import Instructor, Student
from .models import CustomUser as User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
# from crispy_forms.helper import *
# from crispy_forms.layout import Layout, Field


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class InstructorRegisterForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = ['user', 'domainId', 'company', 'linkedIn', 'diploma']


class StudentRegisterForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['user', 'studentId', 'degree', 'university', 'linkedIn']


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['aboutme', 'gender', 'telephone', 'address', 'image']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'input-name', 'placeholder': 'name'}))
    email_address = forms.EmailField(max_length=150, widget=forms.TextInput(attrs={'id': 'input-email', 'placeholder': 'Email Address'}))
    subject = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'id': 'input-subject', 'placeholder': 'Subject'}))
    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'id': 'input-message', 'placeholder': 'Message'}))