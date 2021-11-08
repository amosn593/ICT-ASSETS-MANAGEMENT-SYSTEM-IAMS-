from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

regions = [
    ('SOUTHERN REGION','SOUTHERN REGION'),
    ('NAIROBI','NAIROBI'),
    ('CENTRAL','CENTRAL'),
]

class UserRegistrationForm(UserCreationForm):
    email = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            "username":"Staff Number",
            "email":"Staff Email",
        }

class ProfileForm(forms.ModelForm):
          
    class Meta:
        model = Profile_2
        fields = ['name', 'region']
        labels = {
            "name":"Staff Name",
            "region":"Region",
        }