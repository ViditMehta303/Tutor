from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models import DiagnosticTest, Question, StudentAnswer, DiagnosticResult
from accounts.models import StudentProfile


@login_required
def start_diagnostic(request):
    # Get logged-in student profile
    profile = StudentProfile.objects.get(user=request.user)

    if profile.grade_level is None:
        return redirect("select_grade")

    # Get the diagnostic test for the student's grade
    test = DiagnosticTest.objects.filter(grade_level=profile.grade_level).first()


    if not test:
        return render(request, "core/student/no_test_available.html")

    # 🔒 BLOCK RETAKE: check if result already exists
    existing_result = DiagnosticResult.objects.filter(
        student=profile,
        test=test
    ).order_by("-created_at").first()

    if existing_result:
        return render(
            request,
            "core/student/diagnostic_done.html",
            {"result": existing_result},
        )

    # Get questions
    questions = Question.objects.filter(test=test)

    if request.method == "POST":
        correct = 0

        for q in questions:
            selected = request.POST.get(f"question_{q.id}")

            is_correct = selected == q.correct_option
            if is_correct:
                correct += 1

            StudentAnswer.objects.create(
                student=profile,
                question=q,
                selected_option=selected,
                is_correct=is_correct,
            )

        result = DiagnosticResult.objects.create(
            student=profile,
            test=test,
            total_questions=questions.count(),
            correct_answers=correct,
            percent_score=(correct / questions.count()) * 100,
        )

        return redirect("diagnostic_done")

    return render(
        request,
        "core/student/diagnostic_test.html",
        {"questions": questions},
    )


@login_required
def diagnostic_done(request):
    profile = StudentProfile.objects.get(user=request.user)

    result = DiagnosticResult.objects.filter(
        student=profile
    ).order_by("-created_at").first()

    return render(
        request,
        "core/student/diagnostic_done.html",
        {"result": result},
    )
