from django.contrib import admin
from .models import DiagnosticTest, Question, StudentAnswer, DiagnosticResult

admin.site.register(DiagnosticTest)
admin.site.register(Question)
admin.site.register(StudentAnswer)
admin.site.register(DiagnosticResult)
