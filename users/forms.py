from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image

class UserRegisterForm(UserCreationForm):
    # Write down all the additional inputs we want for the form
    email = forms.EmailField()  # default: required = True

    class Meta:
        model = User    # The model that would be affected is the User model
        fields = ['username', 'email', 'password1', 'password2']    # The fields that we want in the form and in what order


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['img', 'raw']