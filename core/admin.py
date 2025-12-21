from django.contrib import admin
from .models import DiagnosticTest, Question, StudentAnswer

admin.site.register(DiagnosticTest)
admin.site.register(Question)
admin.site.register(StudentAnswer)

