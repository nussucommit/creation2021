from django.contrib.auth import authenticate, login, logout, forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.

def register(request):
    form = forms.UserCreationForm()
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
