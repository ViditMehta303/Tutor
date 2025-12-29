from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.forms import StudentRegisterForm
from core.models import StudentProfile, DiagnosticResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import SelectGradeForm
from .models import StudentProfile

def register_student(request):
    """
    GET  -> show registration form
    POST -> create user + student profile, log in, redirect to grade select
    """
    if request.method == "POST":
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            return redirect("select_grade")
    else:
        form = StudentRegisterForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def select_grade(request):
    profile, _created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = SelectGradeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("student_dashboard")
    else:
        form = SelectGradeForm(instance=profile)

    return render(request, "accounts/select_grade.html", {"form": form})


@login_required
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    latest_result = (
        DiagnosticResult.objects
        .filter(student=profile)
        .order_by("-created_at")
        .first()
    )

    context = {
        "profile": profile,
        "latest_result": latest_result,
    }
    return render(request, "core/student/dashboard.html", context)
