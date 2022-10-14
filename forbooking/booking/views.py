
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
import datetime
from .models import *
from .serializers import Bookingserializer,Paymentserializer
from rest_framework.response import Response
import jwt
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.

class Makeappointment(APIView):
    def post(self,request):
        t=request.COOKIES.get('jwt')
        if not t:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            a=jwt.decode(t,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        print('hello')
    
        y=Bookingserializer(data= {
            #'username' :a['username'],
            'patientid':a['patientid'],
            'doctorid':a['doctorid'],
            'doctorname':a['doctorname'],
            'department':a['department'],
            'patientname':a['patientname'],
            'email':a['email'],
            'phone' :a['phone'],
            'gender':a['gender'],
            'appointmentdate':a['appointmentdate'],
            'appointmenttime':a['appointmenttime'],
            'symptoms':a['symptoms']
        })
        y.is_valid(raise_exception=True)
        y.save()
        return Response({"Thanks for making an appoinment with our Organization \n Please Procced to Payment Page....."})#success

class Patientappointment(APIView):
    def get(self,_,pk=None) :
        a = Slot.objects.filter(patientid=pk)
        serializer = Bookingserializer(a,many=True) #to bring list of items
        return Response(serializer.data)  

class Doctorappointments(APIView):
    def get(self,_,pk=None) :
        print(pk)
        a = Slot.objects.filter(doctorid=pk) #appointment id
        print(a.values())
        serializer = Bookingserializer(a,many=True) 
        return Response(serializer.data)  

class Appointmentupdate (APIView):
    def put(self, request, pk=None):
        try:
            appointment_check= Slot.objects.get(id=pk)
        except:
            return Response({'message':"This appointment doesn't exit"})
        token = request.data['jwt']
        Payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        if appointment_check.patientid == Payload['patientid']:
            if appointment_check.appointmentdate <= datetime.date.today():
                return Response ({"You can't edit past appoinment... Please Check your Details"})
            updation = Bookingserializer(appointment_check,data=Payload)
            if updation.is_valid(raise_exception=True):
                updation.save()
                return Response({
                    'message' : 'Dear user you appointment was Updated Successfully...'
        })
        return Response({'message':"Dear user, you cannot update another user\'s appointment"})


    
class Deleteappointment(APIView):
    def delete(self, request):
        token = request.data['jwt']
        print(token)
        Payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        appointment_delete_id = Payload['appointmentid']#manually giving
        try:
            appoindel= Slot.objects.filter(id=appointment_delete_id).first()
        except:
            return Response({'message':"This appointment doesn't exit"})
        if Payload['patientid'] == appoindel.patientid :
            if appoindel.appointmentdate> datetime.date.today():
                appoindel.delete()
                return Response({
                    'message' : "Dear user, Your appointment was deleted successfully. Your money will be refunded within 2 days... "
              })
            else:
                return Response({
                    'Dear User..Your appoinment was completed with our organization... Please check your Details'
                })

        return Response({ 'message':'Dear user, you cannot delete anothers appointment'})

class Payments(APIView):
    def post(self,request):
        t=request.COOKIES.get('jwt')
        if not t:
            raise AuthenticationFailed('Unauthenticated')
        
        try:
            a=jwt.decode(t,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
    
        y =Paymentserializer(data= {
            'patientid':a['patientid'],
            'appointmentid':a['appointmentid'],
            'nameoncard':a['nameoncard'],
            'cardnumber':a['cardnumber'],
            'expirymonth':a['expirymonth'],
            'expiryyear':a['expiryyear'],
            'cvv':a['cvv']
            
           
        })
        
        b=Slot.objects.filter(id=a['appointmentid']).first()
        try:
            if (a['patientid']==(b.patientid)):
                print("hi")
                y.is_valid(raise_exception=True)
                y.save()
                return Response({'payment success'})
            return Response({"payment failed"})
        except AttributeError:
            return Response({"APPointment Doesn't exist...Please enter the correct ID"})
        
        
        
        
        
        
        