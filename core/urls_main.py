from django.urls import path, include

urlpatterns = [
    path("", include("core.urls.student")),
    path("", include("core.urls.tutor")),
]
