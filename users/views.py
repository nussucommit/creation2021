from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm, Form1, Form2, Form3, Form4, Form5, ContactUsForm
from django.contrib.auth.decorators import login_required
from .models import Statement_1, Statement_2, Statement_3, Statement_4, SideChallenge,ContactUs, ChallengeStatus
import boto
from decouple import config
import re
from django.shortcuts import render
from django.http import HttpResponse
import boto
from decouple import config
from django.contrib.auth.decorators import login_required
from .decorators import allowed_users
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


#Frontend Views

def index(request):
    return render(request, "users/frontend/index.html")

def faq(request):
    return render(request, "users/frontend/faq.html")

def rules(request):
    return render(request, "users/frontend/rules.html")

def timeline(request):
    return render(request, "users/frontend/timeline.html")

def legacy(request):
    return render(request, "users/frontend/legacy.html")

def challenge(request):
    return render(request, "users/frontend/challenge.html")

def registration(request):
    return render(request, "users/frontend/registration.html")

def submission(request):
    return render(request, "users/frontend/submission.html")

#Backend Views

@allowed_users(allowed_roles=['admin'])
def inquiries(request):

    queries = ContactUs.objects.all()
    context = {'queries':queries}

    return render(request, "users/backend/inquiries.html",context)

def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
    
    form = ContactUsForm()

    context = {'form': form}
    return render(request, "users/frontend/contact.html", context)

def user(request):
    return render(request, "users/frontend/user.html")


def challenge_statement_1(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement1.pdf')
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(request, "users/frontend/statement1.html", {"pdf_url": pdf_url})

def challenge_statement_2(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement2.pdf') # remember to change back to respective pdf
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(request, "users/frontend/statement2.html", {"pdf_url": pdf_url})

def challenge_statement_3(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    pdf_file_path = bucket.get_key('assets/statement3.pdf') # remember to change back to respective pdf
    pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(request, "users/frontend/statement3.html", {"pdf_url": pdf_url})

def challenge_statement_4(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    # pdf_file_path = bucket.get_key('assets/statement1.pdf') # remember to change back to respective pdf
    # pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(request, "users/frontend/statement4.html")

def side_challenge(request):
    conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
    bucket = conn.get_bucket('creation-2021')
    # pdf_file_path = bucket.get_key('assets/statement1.pdf') # remember to change back to respective pdf
    # pdf_url = pdf_file_path.generate_url(expires_in=600)

    return render(request, "users/frontend/sidestatement.html")


def register(request):
    # If we get a POST request, we instantiate a user creation form with that POST data.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Creates the user in our database (Check admin page to confirm)
            form.save()
            username = form.cleaned_data.get('username')
            to = form.cleaned_data.get('email')
            subject='Thanks for registering'
            message= f'Hey {username}, you have succesfully registered for an account.'
            send_mail(subject,message,'creation.committee@nussucommit.com',[to])
            # Create an alert to tell users that their account has been succesfully created
            messages.success(request, f'You account has been created! Please log in to continue')
            # Redirect to login page so they can login immidiately
            template = render_to_string('users/backend/email_template.html', {'name': form.cleaned_data.get('first_name')})

            email = EmailMessage(
                'Registration Confirmation',
                template,
                settings.EMAIL_HOST_USER,
                [form.cleaned_data.get('email')],
            )
            email.fail_silently = False
            email.send()
            
            return redirect('login')
    # Anything that isn't a POST request, we just create a blank form.
    else:
        form = UserRegisterForm
    return render(request, 'users/backend/register.html', {'form': form})


@login_required
def profile(request):
    def checkSubmission(submissionNumber):
        if not(submissionNumber):
            return
            
        conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
        bucket = conn.get_bucket('creation-2021')

        for submission in submissionNumber:
            img_file_path = bucket.get_key(submission.img)
            submission.img_url = img_file_path.generate_url(expires_in=600)

            raw_file_path = bucket.get_key(submission.raw)
            submission.raw_url = raw_file_path.generate_url(expires_in=600)

        if submissionNumber:
            context['submissions'] = submissionNumber

    context = {}
    submissions=[]

    submission_1 = Statement_1.objects.all()
    submission_1 = list(filter(lambda x: x.user == request.user, submission_1))

    submission_2 = Statement_2.objects.all()
    submission_2 = list(filter(lambda x: x.user == request.user, submission_2))

    submission_3 = Statement_3.objects.all()
    submission_3 = list(filter(lambda x: x.user == request.user, submission_3))

    submission_4 = Statement_4.objects.all()
    submission_4 = list(filter(lambda x: x.user == request.user, submission_4))

    side_challenge = SideChallenge.objects.all()
    side_challenge = list(filter(lambda x:x.user == request.user, side_challenge))

    submissions += submission_1 + submission_2 + submission_3 + submission_4 + side_challenge

    checkSubmission(submissions)

    return render(request, 'users/backend/profile.html',context)

@login_required
def submit(request):
    registered = ChallengeStatus.objects.filter(user == request.user)
    context = {'registered':registered}
    return render(request, "users/backend/submit.html",context)

@login_required
def form(request,pk):
    context = {}
    if pk == 1:
        form = Form1(request.POST, request.FILES)
    elif pk == 2:
        form = Form2(request.POST, request.FILES)
    elif pk == 3:
        form = Form3(request.POST, request.FILES)
    elif pk == 4:
        form = Form4(request.POST, request.FILES)
    else:
        form = Form5(request.POST, request.FILES)
    # If we get a POST request, we instantiate a submission form with that POST data.
    if request.method == 'POST':

        if form.is_valid():
            form.instance.user = request.user

            img_lst = [] 
            for f in request.FILES.getlist('img'): 
                img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            img_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', img_lst[-1]).replace(' ', '_')
            form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/{img_fname}"
            
            raw_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', raw_lst[-1]).replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/{raw_fname}"

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:
        if pk == 1:
            submissions = Statement_1.objects.all()
        elif pk == 2:
            submissions = Statement_2.objects.all()
        elif pk == 3:
            submissions = Statement_3.objects.all()
        elif pk == 4:
            submissions = Statement_4.objects.all()
        else:
            submissions = SideChallenge.objects.all()
        submissions = list(filter(lambda x: x.user == request.user, submissions))

        conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
        bucket = conn.get_bucket('creation-2021')

        for submission in submissions:
            img_file_path = bucket.get_key(submission.img)
            submission.img_url = img_file_path.generate_url(expires_in=600)

            raw_file_path = bucket.get_key(submission.raw)
            submission.raw_url = raw_file_path.generate_url(expires_in=600)

        if submissions:
            context['submissions'] = submissions
            
        context['form'] = form
    return render(request, "users/backend/form1.html", context)