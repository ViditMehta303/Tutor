from django.urls import path, include

urlpatterns = [
    path("diagnostic/", include("core.urls.diagnostic")),
    path("tutor/", include("core.urls.tutor")),
]
