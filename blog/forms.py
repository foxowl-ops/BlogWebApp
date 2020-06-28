from django import forms
from blog.models import Category, Post
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from tinymce.models import HTMLField


class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required= False)
    phone_no = forms.RegexField(required= False,regex="^[6-9]\d{9}$")

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email') and not cleaned_data.get('phone_no'):
            raise forms.ValidationError("Enter either email or phone number or both", code= 'invalid')



class RegisterForm(forms.Form):
    gender_choices = (('M','Male'),('F','Female'))
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=32, min_length=8, widget= forms.PasswordInput)
    confirm_password = forms.CharField(max_length=32, min_length=8, widget = forms.PasswordInput)
    gender = forms.ChoiceField(choices= gender_choices, widget= forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('password and confirmed password do not match', code='mismatch')


    def clean_username(self):
        data = self.cleaned_data.get('username')
        for x in data:
            if not x.isalpha():
                if not x.isdigit():
                    if x not in ['@','_']:
                        raise forms.ValidationError('Username can have only two special characters @ and _', code= 'mismatch')
        return data



class PostForm(forms.ModelForm):
    class Meta:
        content = forms.CharField(widget = forms.Textarea(attrs={'class':'input'}))
        model = Post
        fields = ('title','content','status', 'category', 'image')
        widgets = {
            'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        slug = slugify(title)
        try:
            post = Post.objects.get(slug = slug)
            raise forms.ValidationError("Title already exists", code='invalid')
        except ObjectDoesNotExist:
            return title

    def clean_image(self):
        img = self.cleaned_data.get('image')
        if img:
            if img.size < 1048576*3:
                return img
            else:
                raise forms.ValidationError("image size should be less than 1 MB", code = "inavlid")

