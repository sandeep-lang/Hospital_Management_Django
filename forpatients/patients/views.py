from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
import requests
from .models import User

# Create your views here.
class Registration(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("Accounted Created Succesfully...Please Login To Continue......")
class Login(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        username  = email.rpartition('@')
        username = username[0] 

        if user is None:
            raise AuthenticationFailed("No User Found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password") 

        Payload = {
            'id':  user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(Payload,'secret',algorithm='HS256')
        response = Response() 
        response.set_cookie(key='jwt',value=token,httponly=True)
        response.data = {
            'jwt':token
        }
        return response 

class ViewProfile(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            Payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthneticated')
        user = User.objects.filter(id=Payload['id']).first() 
        serializer = UserSerializer(user)
        return Response(serializer.data)

class Doctorslist(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            Payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        t = requests.get('http://127.0.0.1:8001/api/dlist')
        print(t)
        return Response(t.json())


class MakeAppointment(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated') 
        try:
            Payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        s=Payload['id']
        a={
           
            'patientid':s,
            'doctorid':request.data['doctorid'],
            'doctorname':request.data['doctorname'],
            'department': request.data['department'],
            'patientname':request.data['patientname'],
            'email':request.data['email'],
            'phone':request.data['phone'],
            'gender':request.data['gender'],
            'appointmentdate':request.data['appointmentdate'],
            'appointmenttime':request.data['appointmenttime'],
            'symptoms':request.data['symptoms']
        }
        t=jwt.encode(a,'secret',algorithm='HS256')
        data = {
            'jwt':t 
        }
        response = requests.post("http://127.0.0.1:8002/api/mapp",cookies=data)
        return Response(response)

class ViewAppointments(APIView):
    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            Payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthneticated')
        l=Payload['id']

        t =requests.get('http://127.0.0.1:8002/api/papp/%d'%l)#imp
        return Response(t.json())
        
class AppointmentUpdate(APIView):
    def put(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            Payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        id = Payload['id']
        payPayload = {
            
            'patientid':id,
            'doctorid':request.data['doctorid'],
            'doctorname':request.data['doctorname'],
            'department': request.data['department'],
            'patientname':request.data['patientname'],
            'email':request.data['email'],
            'phone':request.data['phone'],
            'gender':request.data['gender'],
            'appointmentdate':request.data['appointmentdate'],
            'appointmenttime':request.data['appointmenttime'],
            'symptoms':request.data['symptoms']
        }
        t = jwt.encode(payPayload, 'secret', algorithm='HS256') 
        response = Response()
        response.data = {'jwt' : t}
        cookie = {
            'jwt' : t
        }
        new = request.data['appointmentid']# pk appoinment id
        print(new)
        appointment = requests.put('http://127.0.0.1:8002/api/update/%d'%new, data=cookie)
        return Response(appointment.json())

class AppointmentDelete(APIView):
    def delete(self,request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise  AuthenticationFailed("login with correct details")
        try:
            Payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('login again')
        id = Payload['id'] #prsent login user
        print(id)
        Payload = {
            'appointmentid': request.data['appointmentid'],
            'patientid':id,
        }
        t = jwt.encode(Payload,'secret',algorithm='HS256')
        response = Response()
        response.data = {
            'jwt':t 
        }
        cookie = {'jwt':t}
        b = requests.delete('http://127.0.0.1:8002/api/delete',data=cookie)
        return Response(b)


class Payment(APIView):
    def post(self,request):
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated') 
        try:
            Payload =jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')
        
        s=Payload['id']
        a={
            'patientid':s,
            'appointmentid':request.data['appointmentid'],
            'nameoncard':request.data['nameoncard'],
            'cardnumber':request.data['cardnumber'],
            'expirymonth':request.data['expirymonth'],
            'expiryyear':request.data['expiryyear'],
            'cvv':request.data['cvv'],
        }
        t=jwt.encode(a,'secret',algorithm='HS256')
        data = {
            'jwt':t 
        }
        response = requests.post("http://127.0.0.1:8002/api/payment",cookies=data)
        return Response(response)

class Logout(APIView):
    def post(self,request):
        response = Response() 
        response.delete_cookie('jwt') 
        response.data = {
            'message' : "Your Successfully Loggedout"
        }
        return response