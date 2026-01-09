from django.urls import path
from core.views.student import start_diagnostic, diagnostic_test, diagnostic_done

urlpatterns = [
    # /diagnostic/  -> start page
    path("", start_diagnostic, name="start_diagnostic"),

    # /diagnostic/start/ -> also start page (so your link works)
    path("start/", start_diagnostic, name="start_diagnostic_start"),

    # /diagnostic/test/
    path("test/", diagnostic_test, name="diagnostic_test"),

    # /diagnostic/done/
    path("done/", diagnostic_done, name="diagnostic_done"),
]
