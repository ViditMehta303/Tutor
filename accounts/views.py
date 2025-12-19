from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import StudentRegisterForm
from .models import StudentProfile
from .forms_grade import GradeSelectForm


def register_student(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(username=username, email=email, password=password)

            # Create blank student profile
            StudentProfile.objects.create(user=user)

            # Auto-login after register
            login(request, user)

            # Send student to grade selection
            return redirect("select_grade")
    else:
        form = StudentRegisterForm()

    return render(request, "accounts/register_student.html", {"form": form})

@login_required
def select_grade(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = GradeSelectForm(request.POST)
        if form.is_valid():
            profile.grade_level = int(form.cleaned_data["grade_level"])
            profile.save()
            return redirect("student_dashboard")
    else:
        form = GradeSelectForm()

    return render(request, "accounts/select_grade.html", {"form": form})

@login_required
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if profile.grade_level is None:
        return redirect("select_grade")

    return render(request, "accounts/student_dashboard.html", {"profile": profile})