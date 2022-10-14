from django.urls import path 
from .views import *

urlpatterns = [
    path('mapp',Makeappointment.as_view()),#mapp-->MAKEAPPOINMENT
    path('papp/<int:pk>',Patientappointment.as_view()),
     path('dapp/<int:pk>',Doctorappointments.as_view()),
     path('update/<int:pk>',Appointmentupdate.as_view()),
     path('delete',Deleteappointment.as_view()),
     path('payment',Payments.as_view())


]