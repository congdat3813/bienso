from django.urls import path
 
from .views import *
app_name = 'polls'
urlpatterns = [ 
     path('home/', home, name='home'),
     path('Open/', Open, name='Open'),
     path('Close/', Close, name='close'),
     path('customer/', customer, name='customer'),
     path('customer/<int:id>/', cus_info, name='cus_info'),
]
