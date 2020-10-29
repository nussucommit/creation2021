from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

def register(request):
    # If we get a POST request, we instantiate a user creation form with that POST data.
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Creates the user in our database (Check admin page to confirm)
            form.save()
            username = form.cleaned_data.get('username')
            # Create an alert to tell users that their account has been succesfully created
            messages.success(request, f'Account created for {username}! Please login to continue')
            # Redirect to login page so they can login immidiately
            return redirect('users:submit')
    # Anything that isn't a POST request, we just create a blank form.
    else:
        form = UserRegisterForm
    return render(request, 'users/register.html', {'form': form})

def submit(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "users/user.html", context)

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("users:submit"))    # need to specify users: because there are 2 apps to choose from.
    else:
        return render(request, "users/login.html", {"message": "Invalid credentials. Please try again"})

def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})
