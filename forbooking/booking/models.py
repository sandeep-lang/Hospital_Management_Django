from asyncio.windows_events import NULL
from email.policy import default
from enum import unique
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.exceptions import ValidationError
TIMEPERIOD= (
    ('09:30-10:00','09:30-10:00'),
    ('10:00-10:30','10:00-10:30'),
    ('10:30-11:00','10:30-11:00'),
    ('11:00-11:30','11:00-11:30'),
    ('11:30-12:00','11:30-12:00'),
    ('13:00-13:30','13:00-13:30'),
    ('13:30-14:00','13:30-14:00'),
    ('14:00-14:30','14:00-14:30'),
    ('14:30-15:00','14:30-15:00'),
    ('15:00-15:30','15:00-15:30'),
    ('15:30-16:00','15:30-16:00'),
    ('16:00-16:30','16:00-16:30'),
    ('16:30-17:00','16:30-17:00'),
    ('17:00-17:30','17:00-17:30'),
    ('17:30-18:00','17:30-18:00'),
    ('18:00-18:30','18:00-18:30'),
    )
    
GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('others', 'others'),
)

class Slot(models.Model):
    patientid = models.IntegerField()
    doctorid = models.IntegerField()
    doctorname = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    patientname = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    appointmentdate = models.DateField()
    appointmenttime=models.CharField(max_length=30, choices=TIMEPERIOD)
    symptoms = models.CharField(max_length=200)

    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = []

class Payment(models.Model):
    patientid = models.CharField(max_length=10)
    appointmentid =models.ForeignKey(Slot,on_delete=models.CASCADE, null=True)
    nameoncard = models.CharField(max_length=255)
    cardnumber = models.CharField(max_length=16)
    expirymonth = models.CharField(max_length=4)
    expiryyear = models.CharField(max_length=6)
    cvv = models.CharField(max_length=3, unique = True)
