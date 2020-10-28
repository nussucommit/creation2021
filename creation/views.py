from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "creation/index.html")

def faq(request):
    return render(request, "creation/faq.html")

def rules(request):
    return render(request, "creation/rules.html")

def timeline(request):
    return render(request, "creation/timeline.html")

def legacy(request):
    return render(request, "creation/legacy.html")

def challenge(request):
    return render(request, "creation/challenge.html")

def registration(request):
    return render(request, "creation/registration.html")

def submission(request):
    return render(request, "creation/submission.html")

def contact(request):
    return render(request, "creation/contact.html")