from django.urls import path, include

urlpatterns = [
    path("diagnostic/", include("core.urls.diagnostic")),
]
