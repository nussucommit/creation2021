from django.contrib.auth import authenticate, login, logout, forms, get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
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
import requests
import json



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

    User = get_user_model()
    users = User.objects.all()
    context['total'] = len(users)

    register1 = len(list(filter(lambda x: x.challengestatus.register1, users)))
    register2 = len(list(filter(lambda x: x.challengestatus.register2, users)))
    register3 = len(list(filter(lambda x: x.challengestatus.register3, users)))
    register4 = len(list(filter(lambda x: x.challengestatus.register4, users)))
    registerSide = len(list(filter(lambda x: x.challengestatus.registerSide, users)))

    context['register1'] = register1
    context['register2'] = register2
    context['register3'] = register3
    context['register4'] = register4
    context['registerSide'] = registerSide

    uniqueSubmitter = len(list(filter(lambda x: x.challengestatus.submit1 or x.challengestatus.submit2 or x.challengestatus.submit3
    or x.challengestatus.submit4 or x.challengestatus.submitSide, users)))
    submit1 = len(list(filter(lambda x: x.challengestatus.submit1, users)))
    submit2 = len(list(filter(lambda x: x.challengestatus.submit2, users)))
    submit3 = len(list(filter(lambda x: x.challengestatus.submit3, users)))
    submit4 = len(list(filter(lambda x: x.challengestatus.submit4, users)))
    submitSide = len(list(filter(lambda x: x.challengestatus.submitSide, users)))

    context['uniqueSubmitter'] = uniqueSubmitter
    context['submit1'] = submit1
    context['submit2'] = submit2
    context['submit3'] = submit3
    context['submit4'] = submit4
    context['submitSide'] = submitSide

    return render(request, "users/backend/inquiries.html", context)

def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)
        captcha_token = request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = settings.RECAPTCHA_PRIVATE_KEY
        cap_data = {"secret":cap_secret, "response":captcha_token}
        cap_server_response = requests.post(url=cap_url, data =cap_data)
        cap_json = json.loads(cap_server_response.text)
        print(cap_server_response.text)
        if cap_json['success'] == False:
            messages.warning(request,"Verify Captcha")
            redirect(reverse('users:contact'))
        else:
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
    return render(request, "users/frontend/statement4.html")

def side_challenge(request):
    return render(request, "users/frontend/sidestatement.html")

@login_required
def signup_statement_1(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        if hasattr(current_user, 'challengestatus'):
            status = ChallengeStatus.objects.get(user = current_user)
            status.register1 = True
            status.save()
        else:
            status = ChallengeStatus(user = current_user, register1=True)
            status.save()

        to = current_user.email
        email = EmailMessage(
                'Challenge Statement Registration Confirmation',
                'Succesfully registered for challenge statement 1',
                settings.EMAIL_HOST_USER,
                [to],
            )
        email.fail_silently = False
        email.send()

        conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
        bucket = conn.get_bucket('creation-2021')
        pdf_file_path = bucket.get_key('assets/statement1.pdf')
        pdf_url = pdf_file_path.generate_url(expires_in=600)
        return render(request, "users/frontend/statement1.html", {"pdf_url": pdf_url})
    return render(request, "users/frontend/signup1.html")

@login_required
def signup_statement_2(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        if hasattr(current_user, 'challengestatus'):
            status = ChallengeStatus.objects.get(user = current_user)
            status.register2 = True
            status.save()
        else:
            status = ChallengeStatus(user = current_user, register2=True)
            status.save()

        to = current_user.email
        email = EmailMessage(
                'Challenge Statement Registration Confirmation',
                'Succesfully registered for challenge statement 2',
                settings.EMAIL_HOST_USER,
                [to],
            )
        email.fail_silently = False
        email.send()

        conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
        bucket = conn.get_bucket('creation-2021')
        pdf_file_path = bucket.get_key('assets/statement2.pdf') # remember to change back to respective pdf
        pdf_url = pdf_file_path.generate_url(expires_in=600)
        return render(request, "users/frontend/statement2.html", {"pdf_url": pdf_url})

    return render(request, "users/frontend/signup2.html")

@login_required
def signup_statement_3(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        if hasattr(current_user, 'challengestatus'):
            status = ChallengeStatus.objects.get(user = current_user)
            status.register3 = True
            status.save()
        else:
            status = ChallengeStatus(user = current_user, register3=True)
            status.save()

        to = current_user.email
        email = EmailMessage(
                'Challenge Statement Registration Confirmation',
                'Succesfully registered for challenge statement 3',
                settings.EMAIL_HOST_USER,
                [to],
            )
        email.fail_silently = False
        email.send()

        conn = boto.connect_s3(config('AWS_ACCESS_KEY_ID'), config('AWS_SECRET_ACCESS_KEY'))
        bucket = conn.get_bucket('creation-2021')
        pdf_file_path = bucket.get_key('assets/statement3.pdf') # remember to change back to respective pdf
        pdf_url = pdf_file_path.generate_url(expires_in=600)

        return render(request, "users/frontend/statement3.html", {"pdf_url": pdf_url})
    return render(request, "users/frontend/signup3.html")

@login_required
def signup_statement_4(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        if hasattr(current_user, 'challengestatus'):
            status = ChallengeStatus.objects.get(user = current_user)
            status.register4 = True
            status.save()
        else:
            status = ChallengeStatus(user = current_user, register4=True)
            status.save()

        to = current_user.email
        email = EmailMessage(
                'Challenge Statement Registration Confirmation',
                'Succesfully registered for challenge statement 4',
                settings.EMAIL_HOST_USER,
                [to],
            )
        email.fail_silently = False
        email.send()

        return render(request, "users/frontend/statement4.html")
    return render(request, "users/frontend/signup4.html")

@login_required
def signup_side_statement(request):
    if request.method == 'POST':
        current_user = User.objects.get(username = request.user.username)
        if hasattr(current_user, 'challengestatus'):
            status = ChallengeStatus.objects.get(user = current_user)
            status.registerSide = True
            status.save()
        else:
            status = ChallengeStatus(user = current_user, registerSide=True)
            status.save()

        to = current_user.email
        email = EmailMessage(
                'Challenge Statement Registration Confirmation',
                'Succesfully registered for side challenge statement',
                settings.EMAIL_HOST_USER,
                [to],
            )
        email.fail_silently = False
        email.send()

        return render(request, "users/frontend/sidestatement.html")
    return render(request, "users/frontend/signupside.html")


def register(request):
    # If we get a POST request, we instantiate a user creation form with that POST data.
    if request.user.is_authenticated:
        alert="You are alrd signed in!"
        return redirect('users:index')
        
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Creates the user in our database (Check admin page to confirm)
            form.save()
            username = form.cleaned_data.get('username')
            to = form.cleaned_data.get('email')
            name = form.cleaned_data.get('first_name')
            status = ChallengeStatus(user = User.objects.get(username = username))
            status.save()
            # Create an alert to tell users that their account has been succesfully created
            messages.success(request, f'You account has been created! Please log in to continue')
            
            email = EmailMessage(
                'Registration Confirmation',
                f'Hi {name}! Thank you for registering for Creation 2021',
                settings.EMAIL_HOST_USER,
                [to],
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
            # img_file_path = bucket.get_key(submission.img)
            # submission.img_url = img_file_path.generate_url(expires_in=600)

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
    current_user = User.objects.get(username = request.user.username)
    if not hasattr(current_user,'challengestatus'):
        status = ChallengeStatus(user = current_user)
        
    return render(request, "users/backend/submit.html")

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
        # captcha_token = request.POST.get("g-recaptcha-response")
        # cap_url = "https://www.google.com/recaptcha/api/siteverify"
        # cap_secret = settings.RECAPTCHA_PRIVATE_KEY
        # cap_data = {"secret":cap_secret, "response":captcha_token}
        # cap_server_response = requests.post(url=cap_url, data =cap_data)
        # cap_json = json.loads(cap_server_response.text)
        # print(cap_server_response.text)
        # if cap_json['success'] == False:
        #     messages.warning(request,"Verify Captcha")
        # else:
        if form.is_valid():
            form.instance.user = request.user
            current_user = User.objects.get(username = request.user.username)
            status = ChallengeStatus.objects.get(user=current_user)
            if pk == 1:
                status.submit1 = True
            elif pk == 2:
                status.submit2 = True
            elif pk == 3:
                status.submit3 = True
            elif pk == 4:
                status.submit4 = True
            else:
                status.submitSide = True
            status.save()
            
            # img_lst = [] 
            # for f in request.FILES.getlist('img'): 
            #     img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            # img_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', img_lst[-1]).replace(' ', '_')
            # form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/{img_fname}"
            
            raw_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', raw_lst[-1]).replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/{raw_fname}"

            username = current_user.username
            to = current_user.email
            name = current_user.first_name
            
            email = EmailMessage(
                'Submission Confirmation',
                f'Hi! Thank you for submitting your work for Creation 2021',
                settings.EMAIL_HOST_USER,
                [to],
            )
            email.fail_silently = False
            email.send()

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:   
        context['form'] = form
    return render(request, "users/backend/form1.html", context)