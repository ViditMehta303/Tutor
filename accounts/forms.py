from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentProfile

class StudentRegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "field-input", "placeholder": "Username"}),
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "field-input", "placeholder": "Password"}),
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "field-input", "placeholder": "Confirm password"}),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
class SelectGradeForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["grade_level"]