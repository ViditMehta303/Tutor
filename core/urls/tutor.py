from django.urls import path
from core.views.tutor import tutor_students, tutor_student_detail

urlpatterns = [
    path("students/", tutor_students, name="tutor_students"),
    path("students/<int:student_id>/", tutor_student_detail, name="tutor_student_detail"),
]
