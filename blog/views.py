from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Multi Author Blogging Platform")