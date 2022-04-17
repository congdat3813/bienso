import django.contrib.auth
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, redirect
from .models import *
from django.urls import reverse
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate
from django.http import HttpResponse
from importlib import reload
from django.shortcuts import render
from mysite.wsgi import *

def home(request):
    # GateDB.receiveServer(1)
    # GateDB.receiveServer(2)
    # data=readfile()
    data_file = open('polls/static/txt/bienso.txt', 'r')       
    data = data_file.read()
    print(data)
    data_file.close()
    CamDB.updateCam(1,"static/image/gg.jpg","123")
    rec1 = Gate.objects.get(id=1)
    rec2 = Gate.objects.get(id=2)
    rec3=Cam.objects.get(id=1)
    context = {"item1": rec1,"item2": rec2, "item3":rec3, 'file_content': data}
    return render(request, "home.html", context)


def Open(request):
    import json
    id = json.loads(request.body)
    print("id: ",id)
    GateDB.updateServer(id,'1')
    # redirect('polls/home/')
    return JsonResponse(True, safe=False)

def Close(request):
    import json
    id = json.loads(request.body)
    print("id: ",id)
    GateDB.updateServer(id,'0')
    # redirect('polls/home/')
    return JsonResponse(True, safe=False)


    
def updateGatetoServer(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        state = request.POST.get('state')
        if id == "1":
            GateDB.updateServer(1,state)
        if id == "2":
            aio.send('microbit-led', state)
    return redirect('/home/')

def customer(request):
    rec = Customer.objects.all()
    context = {"item": rec}
    return render(request, "customer.html", context)

def cus_info(request, id):
    rec = Customer.objects.get(id=id)
    context = {"item": rec}
    return render(request, "cus_info.html", context)

def updatecus(request, id):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        bdate = request.POST.get('bdate')
        name = request.POST.get('name')
        cmnd = request.POST.get('cmnd')
        bienso = request.POST.get('bienso')
        sogiayto = request.POST.get('sogiayto')
        CustomerDB.update_cus(id,phone,bdate,name,cmnd,bienso,sogiayto)
        return redirect('customer/<int:id>/')


    