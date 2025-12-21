from django.urls import path
from .views import start_diagnostic, diagnostic_done

urlpatterns = [
    path("", start_diagnostic, name="home"),  # optional: if you want home to go to diagnostic (change later if you want)
    path("diagnostic/start/", start_diagnostic, name="start_diagnostic"),
    path("diagnostic/done/", diagnostic_done, name="diagnostic_done"),
]
