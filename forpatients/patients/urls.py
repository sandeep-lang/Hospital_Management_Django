
from django.urls import path
from .views import *

urlpatterns = [
    path('register',Registration.as_view()),
    path('login',Login.as_view()),
    path('profile',ViewProfile.as_view()),
    path('pprofile',ViewAppointments.as_view()),
    path('logout',Logout.as_view()),
    path('papp',MakeAppointment.as_view()),#appoinmentview --> URL
    path('update',AppointmentUpdate.as_view()),
    path('delete',AppointmentDelete.as_view()),
    path('doclist',Doctorslist.as_view()),
    path('payment',Payment.as_view())

]