from django.urls import path
from .views import register_student, select_grade, student_dashboard

urlpatterns = [
    path("register/", register_student, name="register_student"),
    path("student/grade/", select_grade, name="select_grade"),
    path("student/dashboard/", student_dashboard, name="student_dashboard"),
]
