from django.contrib import admin
from core.models import StudentProfile, DiagnosticQuestion, DiagnosticAnswer


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "grade_level")
    search_fields = ("user__username", "user__email")
    list_filter = ("grade_level",)


@admin.register(DiagnosticQuestion)
class DiagnosticQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "grade_level", "text", "correct_option")
    list_filter = ("grade_level", "correct_option")
    search_fields = ("text",)


@admin.register(DiagnosticAnswer)
class DiagnosticAnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "question", "selected_option", "is_correct", "created_at")
    list_filter = ("is_correct", "selected_option", "question__grade_level")
    search_fields = ("student__user__username", "question__text")
