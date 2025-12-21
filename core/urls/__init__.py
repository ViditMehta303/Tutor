from django.urls import include, path

urlpatterns = [
    path("", include("core.urls.student")),
    path("", include("core.urls.tutor")),
]
