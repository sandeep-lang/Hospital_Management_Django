from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Doctors(AbstractUser):
    doctorname = models.CharField(max_length=200)
    doctoremail = models.EmailField(max_length=200,unique=True)
    Department = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=200)
    username = models.CharField(max_length=200,unique=True)

    REQUIRED_FIELDS = []

