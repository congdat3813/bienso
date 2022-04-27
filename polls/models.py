from email.mime import application
from django.db import models
import random
from django.utils import timezone
import  sys
from Adafruit_IO import Client, Feed, RequestError
from Adafruit_IO import MQTTClient
from polls.lp_extractor.model import *
AIO_FEED_ID = "microbit-temp"
AIO_USERNAME = "t2001kiet"
AIO_KEY = "aio_VYbf70nmKSXUOT2XMWc1FAkRE6js"

ex=LPExtractorModel(debug=False)

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe(AIO_FEED_ID)

def subscribe(client, userdata, mid, granted_qos):
    print("Subscribe thanh cong ...")


def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit(1)


def message(client, feed_id, payload):
    print("Nhan du lieu: "+ feed_id + payload)

client = MQTTClient(AIO_USERNAME , AIO_KEY)
aio = Client(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()

def getValue(microbit):
    a=aio.receive(microbit)
    return a.value

class GateDB:
    @staticmethod
    def get_Gate(id):
        return Gate.objects.get(id=id)
    
    @staticmethod
    def update_Gate(id, state):
        if id==1:
            if state=='0':
                Gate.objects.get(id=id).update(False)
            elif state=='1':
                Gate.objects.get(id=id).update(True)
        if id==2:
            if state=='2':
                Gate.objects.get(id=id).update(False)
            elif state=='3':
                Gate.objects.get(id=id).update(True)
        
    @staticmethod    
    def updateServer(id, state):
        print("updateServer: ",id,state)
        aio.send('microbit-led', state)
        if id==1:
            if state=='0':
                Gate.objects.get(id=id).update(False)
            elif state=='1':
                Gate.objects.get(id=id).update(True)
        if id==2:
            if state=='2':
                Gate.objects.get(id=id).update(False)
            elif state=='3':
                Gate.objects.get(id=id).update(True)

    @staticmethod
    def receiveServer(id):
        
        if id == 1:
            value=0
            value=getValue('microbit-led')
            if value=='0':
                Gate.objects.get(id=id).update(False)
            elif value=='1':
                Gate.objects.get(id=id).update(True)
        elif id == 2:
            value=2
            value=getValue('microbit-led')
            if value=='2':
                Gate.objects.get(id=id).update(False)
            elif value=='3':
                Gate.objects.get(id=id).update(True)
        
class Gate(models.Model):
    dvname = models.CharField(max_length=10)
    state = models.BooleanField(default=False)
    
    def update(self, state):
        self.state = state
        super().save()
class CamDB:
    @staticmethod
    def updateCam(id_gate,img,bienso):
        Cam.objects.get(id_gate=id_gate).update(img,bienso)

class Cam(models.Model):
    id_gate = models.IntegerField() 
    img = models.ImageField(upload_to='static/image',height_field=None,width_field=None, max_length=100,blank=True)
    imgtime = models.DateTimeField()
    bienso=models.CharField(max_length=15)
    def update(self,img,bienso):
        self.img=img
        self.bienso= bienso
        self.imgtime = timezone.now()
        super(Cam,self).save()
class CustomerDB:
    @staticmethod
    def get_cus_list():
        return Customer.objects.all()

    @staticmethod
    def get_cus_info(id_cus):
        return Customer.objects.get(id=id_cus)
    
    @staticmethod
    def update_cus(id_cus,phone,bdate,name,cmnd,bienso,sogiayto):
        Customer.objects.get(id=id_cus).update(phone=phone,bdate=bdate,name=name,cmnd=cmnd,bienso=bienso,sogiayto=sogiayto)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    avt =  models.ImageField(upload_to='static/image/people',height_field=None,width_field=None, max_length=100,blank=True)
    bdate= models.DateField()
    phone = models.CharField(max_length=10)
    cmnd = models.CharField(max_length=15)
    
    bienso = models.CharField(max_length=15)
    anhbien =  models.ImageField(upload_to='static/image/bks',height_field=None,width_field=None, max_length=100,blank=True)
    sogiayto = models.CharField(max_length=255,blank=True)
    anhxe =  models.ImageField(upload_to='static/image/xe',height_field=None,width_field=None, max_length=100,blank=True)
    
    def update(self,phone,bdate,name,cmnd,bienso,sogiayto):
        self.phone = phone
        self.bdate = bdate
        self.name = name
        self.cmnd = cmnd
        self.bienso = bienso
        self.sogiayto = sogiayto
        super().save()
        
class ParkingDB:
    @staticmethod
    def create_parking(id_cus, id_gate, imgtime, bienso):
        Parking.objects.create(id_cus=id_cus, id_gate=id_gate, imgtime=imgtime, bienso=bienso)
                
class Parking(models.Model):
    id_cus= models.IntegerField()   
    id_gate = models.IntegerField()     
    imgtime = models.DateTimeField(default=timezone.now)
    bienso=models.CharField(max_length=15)
      
class Bienso(models.Model):
    bienso1 = models.CharField(max_length=15)
    bienso2 = models.CharField(max_length=15)
    def updatebien(self,bienso1,bienso2):
        self.bienso1=bienso1
        self.bienso2=bienso2