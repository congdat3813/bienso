from django.urls import path
from .views import *
from django.conf.urls.static import static
app_name = 'polls'
urlpatterns = [ 
     path('home/', home, name='home'),
     path('gate/', gate, name='gate'),
     path('Open/', Open, name='Open'),
     path('Close/', Close, name='close'),
     path('cus/', customer, name='cus'),
     path('cus_create', cus_create, name='cus_create'),
     path('cus/<int:id>/', update_cus, name='cus_info'),
     path('delete/<int:id>/', delete_cus, name='cus_delete'),
     path('history/', history, name='history'),
]