from django.http import HttpResponse

def home(request):
    return HttpResponse("Tutoring Centre App is running ✅")
