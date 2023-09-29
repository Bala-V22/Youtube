from django.db import models
from django.core.validators import MaxValueValidator
import datetime
import os
# Create your models here.


def getFileNameProfile(requset,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    # os.path.join('static/assets/media/',new_filename)
    return os.path.join('static/assets/media/',new_filename)

class registration(models.Model):
    name=models.CharField(max_length=50)
    gmail=models.CharField(max_length=100)
    password=models.CharField(max_length=30) 
    profile=models.ImageField(upload_to=getFileNameProfile, null=True, default='static/assets/media/default-avatar.jpg')   

    def __str__(self):
        return self.name
    

def getFileName(requset,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    # os.path.join('static\assets\upload',new_filename)
    return 'static/assets/upload/'+new_filename
    
class upload(models.Model):
    choose=[
        ('public' , 'Public'),
        ('private' , 'Private'),
    ]

    category_choose=[
        ('gaming', 'Gaming'),
        ('education', 'Education'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('fashion & style', 'Fashion & Style')
    ]

    uid=models.IntegerField(primary_key= False , validators=[MaxValueValidator(9999999999)], null=True)
    image=models.ImageField(upload_to=getFileName,null=True, blank=True)
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=5000, blank=True, null=True)
    url=models.URLField(max_length=100) 
    video_in=models.CharField(max_length=10, choices=choose)
    tags=models.CharField(max_length=500, blank=True, null=True)
    category=models.CharField(choices=category_choose, null=True, max_length=30)

    def __str__(self):
        return  self.title
    

class login_user(models.Model):
    uid=models.IntegerField(null=True)
    user_mail=models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.uid)
    

    

        