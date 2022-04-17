from email.mime import application
from django.db import models
import random
from django.utils import timezone
import  sys
from Adafruit_IO import Client, Feed, RequestError
from Adafruit_IO import MQTTClient

AIO_FEED_ID = ["microbit-temp","microbit-led"]
AIO_USERNAME = "t2001kiet"
AIO_KEY = "aio_cQJA91QSrPQLQEQAsIBsBMRsfH6l"

def connected(client):
    print("Ket noi thanh cong ...")
    for feed in AIO_FEED_ID:
        client.subscribe(feed)

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
        Gate.objects.get(id=id).update(state)
        
    @staticmethod    
    def updateServer(id, state):
        if id == 1:
            aio.send('microbit-temp', state)
        elif id == 2:
            aio.send('microbit-led', state)

    @staticmethod
    def receiveServer(id):
        value=0
        if id == 1:
            value=getValue('microbit-temp')
            if value=='0':
                Gate.objects.get(id=id).update(False)
            else:
                Gate.objects.get(id=id).update(True)
        elif id == 2:
            value=getValue('microbit-led')
            if value=='0':
                Gate.objects.get(id=id).update(False)
            else:
                Gate.objects.get(id=id).update(True)
        
class Gate(models.Model):
    dvname = models.CharField(max_length=10)
    state = models.BooleanField(default=False)
    
    def update(self, state):
        self.state = state
        super().save()
class CamDB:
    @staticmethod
    def updateCam(id,img,bienso):
        Cam.objects.get(id=id).update(img,bienso)

class Cam(models.Model):
    id_gate = models.ForeignKey(Gate, on_delete=models.CASCADE)
    img = models.ImageField(upload_to=None, height_field=None,width_field=None, max_length=100,blank=True)
    imgtime = models.DateTimeField()
    bienso=models.CharField(max_length=10)
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
    username = models.CharField(max_length=255)
    pwd = models.CharField(max_length=255)
    phone = models.CharField(max_length=10)
    bdate= models.DateField()
    name = models.CharField(max_length=255)
    cmnd = models.CharField(max_length=15)
    bienso = models.CharField(max_length=10)
    anhbien = models.ImageField(upload_to=None, height_field=None,width_field=None, max_length=100,blank=True)
    sogiayto = models.CharField(max_length=255)
    anhgiayto1 = models.ImageField(upload_to=None, height_field=None,width_field=None, max_length=100,blank=True)
    anhgiayto2= models.ImageField(upload_to=None, height_field=None,width_field=None, max_length=100,blank=True)
    anhxe = models.CharField(max_length=255,blank=True)
    
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
    def create_parking(id_cus, id_gate, img, imgtime, bienso):
        Parking.objects.create(id_cus=id_cus, id_gate=id_gate, img=img, imgtime=imgtime, bienso=bienso)
                
class Parking(models.Model):
    id_cus= models.ForeignKey(Customer, on_delete=models.CASCADE)    
    id_gate = models.ForeignKey(Gate, on_delete=models.CASCADE)       
    img = models.ImageField(upload_to=None, height_field=None,width_field=None, max_length=100,blank=True)
    imgtime = models.DateTimeField(default=timezone.now)
    bienso=models.CharField(max_length=10)