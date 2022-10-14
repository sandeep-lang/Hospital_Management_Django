from xml.parsers.expat import model
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=200)
    username = None

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
