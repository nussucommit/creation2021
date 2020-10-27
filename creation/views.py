from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request, "index.html")

def faq(request):
    return render(request, "faq.html")

def rules(request):
    return render(request, "rules.html")

def timeline(request):
    return render(request, "timeline.html")

def legacy(request):
    return render(request, "legacy.html")

def challenge(request):
    return render(request, "challenge.html")

def registration(request):
    return render(request, "registration.html")

def submission(request):
    return render(request, "submission.html")

def contact(request):
    return render(request, "contact.html")