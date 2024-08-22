from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class ProfilePic(models.Model):
    profile_pic=models.ImageField(upload_to='DP')
    address=models.TextField()
    username=models.OneToOneField(User,on_delete=models.CASCADE)