from django import forms
from .models import registration, upload
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class registerform(forms.ModelForm):
    name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ',  'type': 'text', 'placeholder': 'Enter Name', 'style':'margin-right: 80px;'}))
    gmail=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'email', 'placeholder': 'Enter Email'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control ', 'type': 'password', 'id': 'show_pass', 'placeholder': 'Enter Password'}))

    class Meta:
        model = registration
        fields=['name', 'gmail', 'password']  

class loginform(forms.ModelForm):
    gmail=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'type': 'email', 'placeholder': 'Enter Email'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control form-control-lg ', 'type': 'password', 'id': 'show_pass', 'placeholder': 'Enter Password'}))

    class Meta:
        model = registration
        fields=['gmail', 'password']           

class uploadform(forms.ModelForm):
    CHOICES = (
        ('public', 'Public'),
        ('Private', 'Private'),
    )

    category_choose=[
        ('gaming', 'Gaming'),
        ('education', 'Education'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('fashion & style', 'Fashion & Style')
    ]

    image=forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control',  'type': 'file'}))
    title=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'type': 'text', 'placeholder': 'Enter Title'}))
    description=forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control',  'type': 'text', 'placeholder': 'Enter Your Video Description'}))
    url=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',  'type': 'text', 'placeholder': 'Enter URL'}))
    video_in=forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control',  'type': 'text'}))
    tags=forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control',  'type': 'text',  'placeholder': 'Enter Video Tags'}))
    category=forms.ChoiceField(choices=category_choose, widget=forms.Select(attrs={'class': 'form-control',  'type': 'text'}))
    
    class Meta:
        model = upload
        fields= ['image','title', 'description', 'url', 'video_in', 'tags', 'category']    


class profileform(forms.ModelForm):
    profile=forms.ImageField(required=False, widget=forms.FileInput(attrs={'id': 'wizard-picture'}))
    # name=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'value': '{{users}}'}))
    class Meta:
        model = registration 
        fields = ['profile']       