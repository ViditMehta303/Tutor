from django.db import models
from accounts.models import StudentProfile

from django.conf import settings
from django.db import models

class DiagnosticTest(models.Model):
    grade_level = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Grade {self.grade_level} Diagnostic"


class Question(models.Model):
    TOPIC_ARITHMETIC = "ARITH"
    TOPIC_FRACTIONS = "FRAC"
    TOPIC_ALGEBRA = "ALGB"
    TOPIC_GEOMETRY = "GEOM"
    TOPIC_WORD_PROBLEMS = "WORD"

    TOPIC_CHOICES = [
        (TOPIC_ARITHMETIC, "Arithmetic"),
        (TOPIC_FRACTIONS, "Fractions"),
        (TOPIC_ALGEBRA, "Algebra"),
        (TOPIC_GEOMETRY, "Geometry"),
        (TOPIC_WORD_PROBLEMS, "Word Problems"),
    ]

    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)

    correct_option = models.CharField(max_length=1)

    topic = models.CharField(max_length=5, choices=TOPIC_CHOICES, default=TOPIC_ARITHMETIC)

    def __str__(self):
        return self.text



class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)  # NEW

    def __str__(self):
        return f"{self.student.user.username} - Q{self.question.id}: {self.selected_option}"


class DiagnosticResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    total_questions = models.PositiveSmallIntegerField()
    correct_answers = models.PositiveSmallIntegerField()
    percent_score = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.test.title} - {self.percent_score}%"






class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="core_student_profile",  # <-- add this
    )
    grade = models.IntegerField(null=True, blank=True)

    # ✅ ADD THIS FIELD
    diagnostic_completed = models.BooleanField(default=False)

    weakest_topic = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return f"StudentProfile({self.user.username})"


# If your diagnostic models live here too, keep them.
# If they are in another file already, leave them there.
class DiagnosticQuestion(models.Model):
    text = models.CharField(max_length=500)
    correct_option = models.CharField(max_length=255, blank=True, default="")

    def __str__(self):
        return self.text


class DiagnosticAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(DiagnosticQuestion, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255, blank=True, default="")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - Q{self.question_id}"
