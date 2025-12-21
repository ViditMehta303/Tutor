from django.urls import path
from core.views.student import start_diagnostic, diagnostic_done

urlpatterns = [
    path("diagnostic/start/", start_diagnostic, name="start_diagnostic"),
    path("diagnostic/done/", diagnostic_done, name="diagnostic_done"),
]
