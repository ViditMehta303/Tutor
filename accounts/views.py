from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import StudentRegisterForm, SelectGradeForm
from core.models import StudentProfile


def register_student(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Ensure profile exists
            StudentProfile.objects.get_or_create(user=user)

            return redirect("select_grade")
    else:
        form = StudentRegisterForm()

    return render(request, "accounts/register_student.html", {"form": form})


@login_required
def select_grade(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SelectGradeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = SelectGradeForm(instance=profile)

    return render(request, "accounts/select_grade.html", {"form": form})
