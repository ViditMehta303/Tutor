from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from core.models import StudentProfile


User = get_user_model()


class StudentRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SelectGradeForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ["grade_level"]
        widgets = {
            "grade_level": forms.Select(attrs={"class": "form-control"}),
        }
