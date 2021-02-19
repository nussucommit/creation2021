from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import SideChallenge, Statement_1, Statement_2, Statement_3, Statement_4, ContactUs
from captcha.fields import ReCaptchaField

class UserRegisterForm(UserCreationForm):
    # Write down all the additional inputs we want for the form
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    email = forms.EmailField()  # default: required = True

    class Meta:
        model = User    # The model that would be affected is the User model
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']    # The fields that we want in the form and in what order


class Form1(forms.ModelForm):
    class Meta:
        model = Statement_1
        fields = ['raw','img']

class Form2(forms.ModelForm):
    class Meta:
        model = Statement_2
        fields = ['raw','img']

class Form3(forms.ModelForm):
    class Meta:
        model = Statement_3
        fields = ['raw','img']
        
class Form4(forms.ModelForm):
    class Meta:
        model = Statement_4
        fields = ['raw','img']

class Form5(forms.ModelForm):
    class Meta:
        model = SideChallenge
        fields = ['raw','img']

class ContactUsForm(forms.ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = ContactUs
        fields = ['name', 'email', 'inquiry']