from email import message
from rest_framework import serializers 
from.models import * 
import datetime
from pytz import timezone
from rest_framework.response import Response


from datetime import timedelta

from rest_framework.validators import UniqueTogetherValidator


class Bookingserializer(serializers.ModelSerializer):
   class Meta:
    model =Slot
    fields = ['id','patientid','doctorid','doctorname','department','patientname','email','phone','gender','appointmentdate','appointmenttime','symptoms']

   validators = [ 
      UniqueTogetherValidator(
         queryset = Slot.objects.all(),
         fields=['doctorid','appointmentdate','appointmenttime'],
         message=("The Slot is already Booked!!! Please Choose Another Day"),#CUSTOM MES OVERIDE
      )
   ]
   def validate(self, data):
      past=datetime.date.today()+timedelta(days=7)
      
      if data['appointmentdate'] <= datetime.date.today():
         raise serializers.ValidationError("Date and time must be  more than today")
      elif data['appointmentdate']>past:
            raise serializers.ValidationError("Date should be within 7days")
            #return Response({"Date should be within 7days"})
            #message =("Date Should be within 7 days")
      else:
         now = data['appointmentdate']
        # a=now.strftime("%A")
         a=now.weekday()
         print(a)
         if a==6:
            raise serializers.ValidationError("No Appointment Slot Available For This Day.. Please Select Another Day ")
      return data
      
class Paymentserializer(serializers.ModelSerializer):
   class Meta:
    model =Payment
    fields = ['patientid','appointmentid','nameoncard','cardnumber','expirymonth','expiryyear','cvv']

   


   
   
   
   