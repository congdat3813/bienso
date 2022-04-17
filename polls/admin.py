from django.contrib import admin
 
# Register your models here.
from .models import *

admin.site.register(Customer)
admin.site.register(Gate)
admin.site.register(Cam)
admin.site.register(Parking)
