from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm, MasterForm, Form1, Form2, Form3
from django.contrib.auth.decorators import login_required
from .models import Statement_1, Statement_2, Statement_3
import boto
from decouple import config
import re


def register(request):
    # If we get a POST request, we instantiate a user creation form with that POST data.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # Creates the user in our database (Check admin page to confirm)
            form.save()
            username = form.cleaned_data.get('username')
            # Create an alert to tell users that their account has been succesfully created
            messages.success(request, f'You account has been created! Please log in to continue')
            # Redirect to login page so they can login immidiately
            return redirect('login')
    # Anything that isn't a POST request, we just create a blank form.
    else:
        form = UserRegisterForm
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def submit(request):
    if request.method == 'POST':
        form = MasterForm(request.POST)
        if form.is_valid():
            statement = form.cleaned_data['statement']
            if statement == '1':
                return redirect('users:1')
            elif statement == '2':
                return redirect('users:2')
            else:
                return redirect('users:3')

    form = MasterForm()
    return render(request, "users/submit.html", {'form': form})



@login_required
def form_1(request):
    context = {}
    # If we get a POST request, we instantiate a submission form with that POST data.
    if request.method == 'POST':
        form = Form1(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user

            img_lst = [] 
            for f in request.FILES.getlist('img'): 
                img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            img_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', img_lst[-1]).replace(' ', '_')
            form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{img_fname}"
            
            raw_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', raw_lst[-1]).replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{raw_fname}"

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:
        submissions = Statement_1.objects.all()
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
            
        form = Form1()
        context['form'] = form
    return render(request, "users/form.html", context)



@login_required
def form_2(request):
    context = {}
    # If we get a POST request, we instantiate a submission form with that POST data.
    if request.method == 'POST':
        form = Form2(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user

            img_lst = [] 
            for f in request.FILES.getlist('img'): 
                img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            img_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', img_lst[-1]).replace(' ', '_')
            form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{img_fname}"
            
            raw_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', raw_lst[-1]).replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{raw_fname}"

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:
        submissions = Statement_2.objects.all()
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
            
        form = Form2()
        context['form'] = form
    return render(request, "users/form.html", context)


@login_required
def form_3(request):
    context = {}
    # If we get a POST request, we instantiate a submission form with that POST data.
    if request.method == 'POST':
        form = Form3(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user

            img_lst = [] 
            for f in request.FILES.getlist('img'): 
                img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            img_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', img_lst[-1]).replace(' ', '_')
            form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{img_fname}"
            
            raw_fname = re.sub('[^a-zA-Z0-9 \n\.]', '', raw_lst[-1]).replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{raw_fname}"

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:
        submissions = Statement_3.objects.all()
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
            
        form = Form3()
        context['form'] = form
    return render(request, "users/form.html", context)