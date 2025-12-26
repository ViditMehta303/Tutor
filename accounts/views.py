from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from accounts.models import StudentProfile
from core.models import DiagnosticResult


def register_student(request):
    """
    Simple student registration.
    After register -> login user -> go to grade selection page.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            return render(request, "accounts/register.html", {
                "error": "Username and password are required."
            })

        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "That username is already taken."
            })

        user = User.objects.create_user(username=username, password=password)
        StudentProfile.objects.create(user=user)

        login(request, user)
        return redirect("select_grade")

    return render(request, "accounts/register.html")


@login_required
def select_grade(request):
    student_profile = StudentProfile.objects.get(user=request.user)

    if request.method == "POST":
        grade_level = request.POST.get("grade_level")
        student_profile.grade_level = grade_level
        student_profile.save()
        return redirect("student_dashboard")

    return render(request, "accounts/select_grade.html", {"student": student_profile})


@login_required
def student_dashboard(request):
    student_profile = StudentProfile.objects.get(user=request.user)

    latest_result = (
        DiagnosticResult.objects
        .filter(student=student_profile)   # ✅ FIX IS HERE
        .order_by("-created_at")
        .first()
    )

    context = {
        "student": student_profile,
        "latest_result": latest_result,
    }
    return render(request, "core/student/dashboard.html", context)
