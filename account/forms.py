from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username','password1','password2','email')