from django.urls import path
from core.views import student

urlpatterns = [
    path("accounts/student/grade/", student.select_grade, name="select_grade"),
    path("accounts/student/dashboard/", student.student_dashboard, name="student_dashboard"),

    path("diagnostic/", student.diagnostic_start, name="start_diagnostic"),
    path("diagnostic/test/", student.diagnostic_test, name="diagnostic_test"),
    path("diagnostic/done/", student.diagnostic_done, name="diagnostic_done"),
]
