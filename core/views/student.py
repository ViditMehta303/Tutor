from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# ✅ CHANGE THESE IMPORTS IF YOUR MODEL NAMES ARE DIFFERENT
from core.models import  DiagnosticAnswer, DiagnosticQuestion
from accounts.models import StudentProfile

@login_required
def select_grade(request):
    student = get_object_or_404(StudentProfile, user=request.user)

    if request.method == "POST":
        grade_value = request.POST.get("grade")
        if grade_value:
            student.grade = int(grade_value)
            student.save()
            return redirect("start_diagnostic")  # ✅ make sure this url name exists

    return render(request, "core/student/select_grade.html", {"student": student})


@login_required
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)

    latest_answers = DiagnosticAnswer.objects.filter(student=student)

    total = latest_answers.count()
    correct = latest_answers.filter(is_correct=True).count()

    score = 0
    if total > 0:
        score = round((correct / total) * 100)

    context = {
        "student": student,
        "score": score,
        "correct": correct,
        "total": total,
    }
    return render(request, "core/student/dashboard.html", context)


@login_required
def diagnostic_start(request):
    profile = get_object_or_404(StudentProfile, user=request.user)

    current_grade = getattr(profile, "grade", None)
    if current_grade is None:
        current_grade = getattr(profile, "grade_level", None)

    if current_grade is None:
        return redirect("select_grade")

    return render(request, "core/student/diagnostic_start.html", {"profile": profile})


@login_required
def diagnostic_test(request):
    """
    Shows questions and handles submission.
    If you already have a different function name for the test page,
    copy the POST logic from here into yours.
    """
    student = get_object_or_404(StudentProfile, user=request.user)

    if student.grade is None:
        return redirect("select_grade")

    if student.diagnostic_completed:
        return redirect("diagnostic_done")

    questions = DiagnosticQuestion.objects.all()

    if request.method == "POST":
        # Clear old answers (optional but common)
        DiagnosticAnswer.objects.filter(student=student).delete()

        for question in questions:
            key = f"q_{question.id}"
            selected = request.POST.get(key, "")

            is_correct = False
            if selected and question.correct_option:
                is_correct = (selected == question.correct_option)

            DiagnosticAnswer.objects.create(
                student=student,
                question=question,
                selected_option=selected,
                is_correct=is_correct,
            )

        # ✅ THIS IS THE KEY FIX: mark diagnostic completed
        student.diagnostic_completed = True
        student.save()

        return redirect("diagnostic_done")

    context = {
        "student": student,
        "questions": questions,
    }
    return render(request, "core/student/diagnostic_test.html", context)


@login_required
def diagnostic_done(request):
    student = get_object_or_404(StudentProfile, user=request.user)

    # If not completed, send them back to start
    if not student.diagnostic_completed:
        return redirect("start_diagnostic")

    answers = DiagnosticAnswer.objects.filter(student=student)

    total = answers.count()
    correct = answers.filter(is_correct=True).count()

    score = 0
    if total > 0:
        score = round((correct / total) * 100)

    context = {
        "student": student,
        "score": score,
        "correct": correct,
        "total": total,
    }
    return render(request, "core/student/diagnostic_done.html", context)
