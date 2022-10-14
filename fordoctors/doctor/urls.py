from django.urls import path
from .views import *

urlpatterns = [
    path('login',Login.as_view()),
    path('dlist',Doctorlist.as_view()),
    path('logout',Logout.as_view()),
    path('dapp',DoctorAppointment.as_view())
]
