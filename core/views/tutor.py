from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from accounts.models import StudentProfile
from core.models import DiagnosticResult, StudentAnswer


def is_tutor(user):
    return user.is_staff


@user_passes_test(is_tutor)
def tutor_students(request):
    students = StudentProfile.objects.select_related("user").all().order_by("user__username")

    rows = []
    for student in students:
        latest = DiagnosticResult.objects.filter(student=student).order_by("-created_at").first()

        weakest_topic = None
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
                topic_rows.append({"topic": topic_label, "percent": percent})

            topic_rows.sort(key=lambda r: r["percent"])
            if topic_rows:
                weakest_topic = topic_rows[0]["topic"]

        rows.append(
            {
                "student": student,
                "latest": latest,
                "weakest_topic": weakest_topic,
            }
        )

    return render(request, "core/tutor/tutor_students.html", {"rows": rows})


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
                # --- Tutor Recommendation Logic ---
        overall_percent = round(latest.percent_score, 1)

        if overall_percent < 40:
            level_label = "Foundation"
            pace_label = "Start slow and build confidence"
        elif overall_percent < 70:
            level_label = "Developing"
            pace_label = "Moderate pace with targeted practice"
        else:
            level_label = "Strong"
            pace_label = "Faster pace with challenge questions"

        weakest_topic = topic_rows[0]["topic"] if topic_rows else "General Maths"
        second_topic = topic_rows[1]["topic"] if len(topic_rows) > 1 else None

        focus_message = f"Focus first on {weakest_topic}."
        if second_topic:
            focus_message = focus_message + f" Then reinforce {second_topic}."

        recommendation = {
            "overall_percent": overall_percent,
            "level_label": level_label,
            "pace_label": pace_label,
            "weakest_topic": weakest_topic,
            "second_topic": second_topic,
            "focus_message": focus_message,
        }

    else:
        answers = []
        topic_rows = []
        recommendation = None

    return render(
        request,
        "core/tutor/tutor_student_detail.html",
        {"student": student, "latest": latest, "answers": answers, "topic_rows": topic_rows},
    )
