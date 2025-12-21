from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import StudentProfile
from .models import DiagnosticTest, Question, StudentAnswer


@login_required
def start_diagnostic(request):
    profile = StudentProfile.objects.get(user=request.user)

    # If grade not selected, send them back
    if profile.grade_level is None:
        return redirect("select_grade")

    test = DiagnosticTest.objects.filter(grade_level=profile.grade_level).first()

    if test is None:
        return render(request, "core/no_test_available.html", {"grade": profile.grade_level})

    questions = Question.objects.filter(test=test)

    if request.method == "POST":
        # Optional: clear previous answers for same grade test so resubmissions don’t duplicate
        StudentAnswer.objects.filter(student=profile, question__test=test).delete()

        for q in questions:
            selected = request.POST.get(f"question_{q.id}")
            if selected is not None and selected != "":
                StudentAnswer.objects.create(
                    student=profile,
                    question=q,
                    selected_option=selected
                )

        return redirect("diagnostic_done")

    return render(request, "core/diagnostic_test.html", {"test": test, "questions": questions})


@login_required
def diagnostic_done(request):
    return render(request, "core/diagnostic_done.html")
