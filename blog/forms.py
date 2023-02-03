from datetime import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor.fields import *
from .models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    password1 = forms.CharField(label ='Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label ='Repetir contraseña', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {k:"" for k in fields}

class UserEditForm(UserCreationForm):
    email = forms.EmailField(label ='Modificar E-Mail')
    password1 = forms.CharField(label ='Contraseña', widget = forms.PasswordInput)
    password2 = forms.CharField(label ='Repetir contraseña', widget = forms.PasswordInput)
    first_name=forms.CharField(label='Modificar Nombre')

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2', 'first_name']
        help_texts = {k:"" for k in fields}

class AvatarForm(forms.Form):
    imagen = forms.ImageField(label="Imagen", required=False)
    class Meta:
        model = Avatar
        fields = ['imagen']

class CrearPublicacion(forms.Form):
    imagen = forms.ImageField(label="Imagen", required=True)
    nombre=forms.CharField(max_length=50)
    categoria=forms.CharField(max_length=50)
    descripcion = RichTextFormField()

class Perfil(forms.Form):
    descripcion = forms.CharField(max_length=200)
    link=forms.CharField(max_length=50)
    imagen = forms.ImageField(label="Imagen", required=False)
    class Meta:
        model = Perfil
        fields = ['descripcion', 'link' , 'imagen']
