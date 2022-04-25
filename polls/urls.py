from django.urls import path
 
from .views import *
app_name = 'polls'
urlpatterns = [ 
     path('home/', home, name='home'),
     path('gate/', gate, name='gate'),
     path('Open/', Open, name='Open'),
     path('Close/', Close, name='close'),
     path('cus/', customer, name='cus'),
     # path('cus/<int:id>/', cus_info, name='cus_info'),
     # path('history/', history, name='history'),
     # path('history/<int:id>/', his_info, name='history'),
]
