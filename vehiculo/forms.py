from django import forms
from .models import VehiculoModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = VehiculoModel
        fields = ('marca', 'modelo', 'serial_carroceria', 'serial_motor', 'categoria', 'precio')

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")