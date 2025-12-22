from django.contrib import admin
from .models import DiagnosticTest, Question, StudentAnswer, DiagnosticResult


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "test", "topic", "correct_option")
    list_filter = ("test", "topic")
    search_fields = ("text",)


admin.site.register(DiagnosticTest)
admin.site.register(StudentAnswer)
admin.site.register(DiagnosticResult)
