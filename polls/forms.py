from django import forms
from .models import Customer, Bienso
#DataFlair
class CusCreate(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        labels = {
            "name": "Họ và tên",
            "avt": "Ảnh đại diện",
            "bdate": "Ngày sinh",
            "phone": "Số điện thoại",
            "cmnd": "Số CMND",
            "bienso": "Biển số xe",
            "anhbien": "Ảnh biển số xe",
            "sogiayto": "Số giấy tờ",
            "anhxe": "Ảnh xe"
        }

class Bienform(forms.ModelForm):
    class Meta:
        model = Bienso
        fields = '__all__'