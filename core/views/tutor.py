from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from accounts.models import StudentProfile
from core.models import DiagnosticResult, StudentAnswer


def is_tutor(user):
    return user.is_staff


@user_passes_test(is_tutor)
def tutor_students(request):
    students = StudentProfile.objects.select_related("user").all()

    latest_results = {}
    for s in students:
        latest = DiagnosticResult.objects.filter(student=s).order_by("-created_at").first()
        latest_results[s.id] = latest

    return render(
        request,
        "core/tutor/tutor_students.html",
        {"students": students, "latest_results": latest_results},
    )


@user_passes_test(is_tutor)
def tutor_student_detail(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)

    latest = DiagnosticResult.objects.filter(student=student).order_by("-created_at").first()

    if latest:
        answers = StudentAnswer.objects.filter(
            student=student,
            question__test=latest.test
        ).select_related("question")

        topic_counts = {}

        for a in answers:
            topic_label = a.question.get_topic_display()

            if topic_label not in topic_counts:
                topic_counts[topic_label] = {"total": 0, "correct": 0}

            topic_counts[topic_label]["total"] += 1
            if a.is_correct:
                topic_counts[topic_label]["correct"] += 1

        topic_rows = []
        for topic_label, counts in topic_counts.items():
            total = counts["total"]
            correct = counts["correct"]
            percent = (correct / total) * 100 if total > 0 else 0

            topic_rows.append(
                {
                    "topic": topic_label,
                    "total": total,
                    "correct": correct,
                    "percent": round(percent, 1),
                }
            )

        topic_rows.sort(key=lambda row: row["percent"])
    else:
        answers = []
        topic_rows = []

    return render(
        request,
        "core/tutor/tutor_student_detail.html",
        {"student": student, "latest": latest, "answers": answers, "topic_rows": topic_rows},
    )
