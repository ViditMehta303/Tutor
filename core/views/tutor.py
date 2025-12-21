from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404

from accounts.models import StudentProfile
from core.models import DiagnosticResult, StudentAnswer


def is_tutor(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_tutor)
def tutor_students(request):
    students = StudentProfile.objects.all().order_by("user__username")

    rows = []
    for student in students:
        latest = DiagnosticResult.objects.filter(student=student).order_by("-created_at").first()
        rows.append({"student": student, "latest": latest})

    return render(request, "core/tutor/tutor_students.html", {"rows": rows})


@user_passes_test(is_tutor)
def tutor_student_detail(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    results = DiagnosticResult.objects.filter(student=student).order_by("-created_at")
    latest = results.first()

    answers = []
    if latest:
        answers = StudentAnswer.objects.filter(
            student=student,
            question__test=latest.test
        ).select_related("question")

    return render(
        request,
        "core/tutor/tutor_student_detail.html",
        {
            "student": student,
            "results": results,
            "latest": latest,
            "answers": answers,
        },
    )
