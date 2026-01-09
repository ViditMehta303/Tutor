from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    GRADE_CHOICES = [
        (1, "Grade 1"),
        (2, "Grade 2"),
        (3, "Grade 3"),
        (4, "Grade 4"),
        (5, "Grade 5"),
        (6, "Grade 6"),
        (7, "Grade 7"),
        (8, "Grade 8"),
        (9, "Grade 9"),
        (10, "Grade 10"),
        (11, "Grade 11"),
        (12, "Grade 12"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile")
    grade_level = models.IntegerField(choices=GRADE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} (Grade {self.grade_level})"


class DiagnosticQuestion(models.Model):
    GRADE_CHOICES = StudentProfile.GRADE_CHOICES

    grade_level = models.IntegerField(choices=GRADE_CHOICES)
    text = models.TextField()

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
    )

    def __str__(self):
        return f"Grade {self.grade_level}: {self.text[:50]}"


class DiagnosticAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(DiagnosticQuestion, on_delete=models.CASCADE)

    selected_option = models.CharField(
        max_length=1,
        choices=[("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")],
    )
    is_correct = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - Q{self.question.id} - {self.selected_option}"
