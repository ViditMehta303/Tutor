from django.db import models
from accounts.models import StudentProfile

class DiagnosticTest(models.Model):
    grade_level = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Grade {self.grade_level} Diagnostic"


class Question(models.Model):
    test = models.ForeignKey(DiagnosticTest, on_delete=models.CASCADE)
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct_option = models.CharField(max_length=1)

    def __str__(self):
        return self.text[:50]


class StudentAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
