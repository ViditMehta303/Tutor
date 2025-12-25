from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("register/", views.register_student, name="register_student"),
    path("student/grade/", views.select_grade, name="select_grade"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),
]
