from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import StudentProfile
from core.models import DiagnosticTest, Question, StudentAnswer, DiagnosticResult


@login_required
def start_diagnostic(request):
    profile = StudentProfile.objects.get(user=request.user)

    if profile.grade_level is None:
        return redirect("select_grade")

    test = DiagnosticTest.objects.filter(grade_level=profile.grade_level).first()

    if test is None:
        return render(
            request,
            "core/student/no_test_available.html",
            {"grade": profile.grade_level},
        )

    questions = Question.objects.filter(test=test)

    if request.method == "POST":
        StudentAnswer.objects.filter(
            student=profile, question__test=test
        ).delete()
        DiagnosticResult.objects.filter(
            student=profile, test=test
        ).delete()

        total = questions.count()
        correct = 0

        for q in questions:
            selected = request.POST.get(f"question_{q.id}")

            if not selected:
                continue

            is_correct = selected.upper() == q.correct_option.upper()
            if is_correct:
                correct += 1

            StudentAnswer.objects.create(
                student=profile,
                question=q,
                selected_option=selected.upper(),
                is_correct=is_correct,
            )

        percent = (correct / total) * 100 if total > 0 else 0

        DiagnosticResult.objects.create(
            student=profile,
            test=test,
            total_questions=total,
            correct_answers=correct,
            percent_score=percent,
        )

        return redirect("diagnostic_done")

    return render(
        request,
        "core/student/diagnostic_test.html",
        {"test": test, "questions": questions},
    )


@login_required
def diagnostic_done(request):
    profile = StudentProfile.objects.get(user=request.user)
    latest_result = (
        DiagnosticResult.objects.filter(student=profile)
        .order_by("-created_at")
        .first()
    )

    return render(
        request,
        "core/student/diagnostic_done.html",
        {"result": latest_result},
    )
