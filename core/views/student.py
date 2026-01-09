from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.models import StudentProfile, DiagnosticQuestion, DiagnosticAnswer


@login_required
def diagnostic_start(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    # If no grade picked, send to grade selection
    if not profile.grade_level:
        return redirect("select_grade")

    # If no questions exist, still show a friendly page
    questions_count = DiagnosticQuestion.objects.filter(grade_level=profile.grade_level).count()
    context = {
        "grade_level": profile.grade_level,
        "questions_count": questions_count,
    }
    return render(request, "core/student/diagnostic_start.html", context)


@login_required
def diagnostic_test(request):
    # get student profile
    profile = StudentProfile.objects.get(user=request.user)

    # load questions for student's grade
    questions = DiagnosticQuestion.objects.filter(grade_level=profile.grade_level)

    if request.method == "POST":
        # clear old answers for re-take (optional but recommended)
        DiagnosticAnswer.objects.filter(student=profile).delete()

        for question in questions:
            selected = request.POST.get(f"q_{question.id}")
            if not selected:
                # if not answered, skip or handle validation
                continue

            is_correct = (selected == question.correct_option)

            DiagnosticAnswer.objects.create(
                student=profile,
                question=question,
                selected_option=selected,
                is_correct=is_correct,
            )

        return redirect("diagnostic_done")  # IMPORTANT: redirect after POST

    return render(request, "core/student/diagnostic_test.html", {"questions": questions})



@login_required
def diagnostic_done(request):
    profile = StudentProfile.objects.get(user=request.user)
    answers = DiagnosticAnswer.objects.filter(student=profile)

    total = answers.count()
    correct = answers.filter(is_correct=True).count()

    return render(
        request,
        "core/student/diagnostic_done.html",
        {"total": total, "correct": correct}
    )


@login_required
def student_dashboard(request):
    """
    Student dashboard after login.
    If grade isn't selected yet, force them to pick grade first.
    """
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        profile = None

    if not profile or not profile.grade_level:
        return redirect("select_grade")

    context = {
        "profile": profile,
    }
    return render(request, "core/student/dashboard.html", context)