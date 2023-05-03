from django.http import HttpResponse, HttpRequest

def home(request):
    return HttpResponse("<h1>wellcome to baham.</h1>")

