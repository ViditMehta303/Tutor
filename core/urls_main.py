# core/urls_main.py
from django.urls import path
from core.views.student import diagnostic_start, diagnostic_test, diagnostic_done

urlpatterns = [
    # Existing / canonical names
    path("diagnostic/", diagnostic_start, name="diagnostic_start"),
    path("diagnostic/test/", diagnostic_test, name="diagnostic_test"),
    path("diagnostic/done/", diagnostic_done, name="diagnostic_done"),

    # Alias names used elsewhere in your code/templates
    path("diagnostic/", diagnostic_start, name="start_diagnostic"),

    # Optional: if you ever visit /diagnostic/start/ (you did earlier)
    path("diagnostic/start/", diagnostic_start, name="diagnostic_start_page"),
]
