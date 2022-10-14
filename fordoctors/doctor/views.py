from rest_framework.views import APIView
from .serializers import *
from . models import*
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
import requests


class Login(APIView):
    def post(self,request):
        username = request.data['username']
        password = request.data['password']

        user = Doctors.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed("User Not Found") 
        
        if str(password)!= user.password:
            raise AuthenticationFailed("Please enter valid password")
        
        Payload = {
            'id':  user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        t = jwt.encode(Payload,'secret',algorithm='HS256')
        response = Response() 
        response.set_cookie(key='jwt',value=t,httponly=True)
        response.data = {
            'jwt':t
        }
        return response

class DoctorAppointment(APIView): 
    def get(self,request):
        token=request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            Payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthneticated')
        l=Payload['id']

        token =requests.get('http://127.0.0.1:8002/api/dapp/%d'% l)
        return Response (token.json())
class Doctorlist(APIView):
    def get(self,_,pk=None):
        a=Doctors.objects.all() 
        serializer = UserSerializer(a,many=True)
        return Response(serializer.data)

class Logout(APIView):
    def post(self,request):
        response = Response() 
        response.delete_cookie('jwt') 
        response.data = {
            'message' : "Your Successfully Loggedout"
        }
        return response