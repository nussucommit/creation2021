from django.shortcuts import render
from django.http import HttpResponse
import boto
from decouple import config
from django.contrib.auth.decorators import login_required
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

def user(request):
    return render(request, "users/user.html")

@login_required
def challenge_statement_1(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement1.pdf')
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(erquest, "creation/statement1.html", {"pdf_url": pdf_url})

@login_required
def challenge_statement_2(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement2.pdf')
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(erquest, "creation/statement2.html", {"pdf_url": pdf_url})

@login_required
def challenge_statement_3(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement3.pdf')
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(erquest, "creation/statement3.html", {"pdf_url": pdf_url})