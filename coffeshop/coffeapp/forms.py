from django import forms
from .models import Users, Orders, Products, Admins, Storage, User

# این فرم مربوط به جدول Users در فایل models.py است
class MyUserCreationForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'full_name', 'email', 'password', 'phone_number']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


    
# این فرم مربوط به جدول Orders در فایل models.py است
class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ('type',)  

# این فرم مربوط به جدول Products در فایل models.py است
class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        exclude= ['id']

# این فرم مربوط به جدول Admins در فایل models.py است
class AdminsForm(forms.ModelForm):
    class Meta:
        model = Admins
        fields = ['username', 'email', 'password']

# این فرم مربوط به جدول Storage در فایل models.py است
class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['name', 'amount']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=10)