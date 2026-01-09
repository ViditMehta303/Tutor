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
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    if not profile.grade_level:
        return redirect("select_grade")

    questions = list(DiagnosticQuestion.objects.filter(grade_level=profile.grade_level).order_by("id"))

    if len(questions) == 0:
        return redirect("diagnostic_start")

    # index in session (simple paging)
    index = request.session.get("diag_index", 0)
    if index < 0:
        index = 0
    if index >= len(questions):
        return redirect("diagnostic_done")

    question = questions[index]

    if request.method == "POST":
        selected = request.POST.get("selected_option")
        if selected in ["A", "B", "C", "D"]:
            is_correct = (selected == question.correct_option)

            DiagnosticAnswer.objects.update_or_create(
                student=profile,
                question=question,
                defaults={"selected_option": selected, "is_correct": is_correct},
            )

            request.session["diag_index"] = index + 1
            return redirect("diagnostic_test")

    context = {
        "question": question,
        "index": index + 1,
        "total": len(questions),
    }
    return render(request, "core/student/diagnostic_test.html", context)


@login_required
def diagnostic_done(request):
    profile, _ = StudentProfile.objects.get_or_create(user=request.user)

    answers = DiagnosticAnswer.objects.filter(student=profile)
    total = answers.count()
    correct = answers.filter(is_correct=True).count()

    # reset session index so they can retake later if you want
    request.session["diag_index"] = 0

    context = {
        "total": total,
        "correct": correct,
    }
    return render(request, "core/student/diagnostic_done.html", context)

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