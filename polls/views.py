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
from .forms import *
from importlib import reload
from django.shortcuts import render
from mysite.wsgi import *
from polls.lp_extractor.model import *
def home(request):
    return render(request, "t/homepage.html")


def gate(request):
    
    try:
        lp= ex.extractLP('polls/static/image/abcd.jpeg')
    except Exception as e: 
        print(e)
        lp= ''
    
    with open('polls/static/txt/1.txt', 'w') as f:
        f.write(lp)
    data_file1 = open('polls/static/txt/1.txt', 'r')       
    data1 = data_file1.read()
    data_file1.close()
    data_file2 = open('polls/static/txt/2.txt', 'r')       
    data2 = data_file2.read()
    data_file2.close()
    
    bienso=Bienso.objects.get(id=1)
    bienso.updatebien(data1,data2)
    #Lay Cam cuoi cung
    cam1=Cam.objects.get(id=1)
    cam2=Cam.objects.get(id=2)
    #Lay Khach hàng qua bien so
    # cus1= Customer.objects.get(bienso=data1)
    # cus2= Customer.objects.get(bienso=data2)
    try:
        cus1= Customer.objects.get(bienso=data1)
    except:
        cus1=None
    try:
        cus2= Customer.objects.get(bienso=data2)
    except:
        cus2=None
    

    # Dieu khien Cam va Gate
    if data1!= cam1.bienso:
        if cus1!= None:
            GateDB.updateServer(1,'1')
            cam1.update("static/image/abcd.jpeg",data1)
            ParkingDB.create_parking(cus1.id,1,cam1.imgtime,cam1.bienso)
    if data2!= cam2.bienso :
        if cus2 != None:
            GateDB.updateServer(2,'3')
            cam2.update("static/image/2.png",data2)
            ParkingDB.create_parking(cus2.id,2,cam2.imgtime,cam2.bienso)
            
    bienso_form = Bienform(request.POST or None, instance = bienso)
    # cam2_form = Camform(request.POST or None, instance = rec4)
    if bienso_form.is_valid():
        print("bien 1,2 trc :",bienso.bienso1,bienso.bienso2)
        bienso_form.save()
        print("bien 1,2 trc :",bienso.bienso1,bienso.bienso2)
        with open('polls/static/txt/1.txt', 'w') as f:
            f.write(bienso.bienso1)
        try:
            cus1= Customer.objects.get(bienso=bienso.bienso1)
        except:
            cus1=None
        if bienso.bienso1!= cam1.bienso:
            if cus1!= None:
                GateDB.updateServer(1,'1')
                cam1.update("static/image/abcd.jpeg",bienso.bienso1)
                ParkingDB.create_parking(cus1.id,1,cam1.imgtime,cam1.bienso)
        with open('polls/static/txt/2.txt', 'w') as f:
            f.write(bienso.bienso2)
        try:
            cus2= Customer.objects.get(bienso=bienso.bienso2)
        except:
            cus2=None
        if bienso.bienso2!= cam2.bienso :
            if cus2!= None:
                GateDB.updateServer(2,'3')
                cam2.update("static/image/2.png",bienso.bienso2)
                ParkingDB.create_parking(cus2.id,2,cam2.imgtime,cam2.bienso)
        # return redirect('../gate/')
    
    context = {"cus1": cus1,"cus2": cus2,"cam1": cam1,"cam2": cam2, 'bienso_form':bienso_form}
    # context = {"item1": rec1,"item2": rec2, "item3":rec3,"item4":rec4, "data1": data1,"data2": data2}
    return render(request, "t/gate.html", context)

# def submit(request,id):
#     bienso1=Bienso.objects.get(id=id)
#     bien1_form = Bienform(request.POST or None, instance = bienso1)
#     if bien1_form.is_valid():
#         bien1_form.save()
#         return redirect('../gate/')

def Open(request):
    import json
    id = json.loads(request.body)
    if id==1:
        GateDB.updateServer(id,'1')
    elif id==2:
        GateDB.updateServer(id,'3')
    
    # redirect('polls/home/')
    return JsonResponse(True, safe=False)

def Close(request):
    import json
    id = json.loads(request.body)
    if id==1:
        GateDB.updateServer(id,'0')
    elif id==2:
        GateDB.updateServer(id,'2')
    # redirect('polls/home/')
    return JsonResponse(True, safe=False)


    
# def updateGatetoServer(request):
#     if request.method == 'POST':
#         id = request.POST.get('id')
#         state = request.POST.get('state')
#         if id == "1":
#             GateDB.updateServer(1,state)
#         if id == "2":
#             aio.send('microbit-led', state)
#     return redirect('/gate/')

def customer(request):
    rec = Customer.objects.all()
    context = {"item": rec}
    return render(request, "t/cus.html", context)

def cus_info(request, id):
    rec = Customer.objects.get(id=id)
    context = {"item": rec}
    return render(request, "t/cus_info.html", context)

# def updatecus(request, id):
#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         bdate = request.POST.get('bdate')
#         name = request.POST.get('name')
#         cmnd = request.POST.get('cmnd')
#         bienso = request.POST.get('bienso')
#         sogiayto = request.POST.get('sogiayto')
#         CustomerDB.update_cus(id,phone,bdate,name,cmnd,bienso,sogiayto)
#         return redirect('cus/<int:id>/')

def cus_create(request):
    upload = CusCreate()
    if request.method == 'POST':
        upload = CusCreate(request.POST , request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('./cus')
        else:
            return redirect('./cus')
    else:
        return render(request, 't/cus_create.html', {'upload_form':upload}) 
      
def update_cus(request, id):
    id = int(id)
    try:
        cus_sel = Customer.objects.get(id = id)
    except Customer.DoesNotExist:
        return redirect('../../cus')
    cus_form = CusCreate(request.POST or None, instance = cus_sel)
    if cus_form.is_valid():
       cus_form.save()
    return render(request, 't/cus_info.html', {'item':cus_form,'sel':cus_sel})

def delete_cus(request, id):
    id = int(id)
    try:
        cus_sel = Customer.objects.get(id = id)
    except Customer.DoesNotExist:
        return redirect('../../cus')
    cus_sel.delete()
    return redirect('../../cus')

def history(request):
    rec = Parking.objects.all().order_by('-imgtime')
    context = {"item": rec}
    return render(request, "t/history.html", context)

# def his_info(request,id):
#     rec = Parking.objects.get(id=id)
#     context = {"item": rec}
#     return render(request, "his_info.html", context)


    