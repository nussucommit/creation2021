from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm, ImageForm
from django.contrib.auth.decorators import login_required
from .models import Image
import pytz

# Create your views here.

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
    # If we get a POST request, we instantiate a submission form with that POST data.
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user = request.user

            # Time changed but the change is not reflected on the display
            #print(form.instance.time)
            #form.instance.time = form.instance.time.astimezone(pytz.timezone('Asia/Singapore'))
            #print(form.instance.time)

            img_lst = [] 
            for f in request.FILES.getlist('img'): 
                img_lst.append(f.name)

            raw_lst = []
            for f in request.FILES.getlist('raw'): 
                raw_lst.append(f.name)

            img_fname = img_lst[-1].replace(' ', '_')
            form.instance.img_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{img_fname}"
            
            raw_fname = raw_lst[-1].replace(' ', '_')
            form.instance.raw_url = f"https://creation-2021.s3.ap-southeast-1.amazonaws.com/img/{raw_fname}"

            form.save()

            # Refreshes the page
            return HttpResponseRedirect(request.path_info)
    # Anything that isn't a POST request, we just create a blank form.
    else:
        submissions = Image.objects.all()
        print(submissions)
        filtered = []
        for submission in submissions:
            if submission.user == request.user:
                filtered.append(submission)

        context = {}
        if filtered:
            context['submissions'] = filtered
        form = ImageForm()
        context['form'] = form
    return render(request, "users/submit.html", context)

