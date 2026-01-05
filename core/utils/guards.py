from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def require_student_profile(view_func):
    """
    Ensures the logged-in user has a StudentProfile.
    If not, redirects to student registration (or login).
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not hasattr(request.user, "studentprofile"):
            messages.error(request, "Student profile not found. Please register first.")
            return redirect("register_student")
        return view_func(request, *args, **kwargs)
    return _wrapped


def require_grade_selected(view_func):
    """
    Ensures the student has selected a grade.
    Adjust field name if your StudentProfile uses something else.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        student = request.user.studentprofile

        # CHANGE THIS if your field name is different:
        # e.g. student.grade_level, student.grade, student.current_grade
        grade_value = getattr(student, "grade", None)

        if not grade_value:
            return redirect("select_grade")

        return view_func(request, *args, **kwargs)
    return _wrapped


def require_no_diagnostic_yet(view_func):
    """
    Used on diagnostic start page:
    If diagnostic already submitted, send to done page.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        student = request.user.studentprofile

        # CHANGE THIS model import / query if your diagnostic model name differs
        from core.models import StudentAnswer  # <-- adjust if needed

        already_submitted = StudentAnswer.objects.filter(student=student).exists()
        if already_submitted:
            return redirect("diagnostic_done")

        return view_func(request, *args, **kwargs)
    return _wrapped


def require_diagnostic_done(view_func):
    """
    Used on dashboard (and done page):
    If diagnostic NOT submitted yet, send to diagnostic start.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        student = request.user.studentprofile

        # CHANGE THIS model import / query if your diagnostic model name differs
        from core.models import StudentAnswer  # <-- adjust if needed

        submitted = StudentAnswer.objects.filter(student=student).exists()
        if not submitted:
            return redirect("start_diagnostic")

        return view_func(request, *args, **kwargs)
    return _wrapped
