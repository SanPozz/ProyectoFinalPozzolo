from django.shortcuts import render, redirect
from datetime import date
import datetime
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView
#Imports Logins
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

def inicio(request):
    publicacion = Publicacion.objects.order_by('-id')[0:3]
    return render(request, "blog/inicio.html", {"publicacion": publicacion,})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            usu=request.POST["username"]
            clave=request.POST["password"]

            usuario=authenticate(username=usu, password=clave)

            if usuario is not None:
                login(request, usuario)
                return render(request, 'blog/inicio.html', {'mensaje':f"Bienvenido {usuario}",'imagen':obtenerAvatar(request)})
            else:
                return render(request, 'blog/login.html', {"form": form, 'mensaje':'Usuario o contraseña incorrecta'})
        else: 
            return render(request, 'blog/login.html', {"form": form,'mensaje':'Formulario Invalido'})
    else:
        form=AuthenticationForm()
        return render(request, 'blog/login.html', {'form':form})

def registro(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            form.save()
            return render(request, 'blog/inicio.html', {'mensaje': f"Usuario {username} creado"})
    else:
        form = UserRegisterForm()
    return render(request, 'blog/registro.html', {"form":form})

@login_required
def editarPerfil(request):
    user=request.user
    if request.method=="POST":
        form=UserEditForm(request.POST)
        if form.is_valid():
            info=form.cleaned_data
            user.first_name=info["first_name"]
            user.last_name=info["last_name"]
            user.email=info["email"]
            user.password1=info["password1"]
            user.password1=info["password2"]
            user.save()
            return render(request, 'blog/inicio.html', {"mensaje": f"Perfil de {user} editado",'imagen':obtenerAvatar(request)})
    else:
        form = UserEditForm(initial={"first_name":user.first_name, "last_name":user.last_name, 'email':user.email})
    return render(request, 'blog/editarPerfil.html', {"form":form, 'usuario':user,'imagen':obtenerAvatar(request)})

@login_required
def agregar_avatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            avatarViejo=Avatar.objects.filter(user=request.user)
            if(len(avatarViejo)>0):
                avatarViejo.delete()
            avatar= Avatar(user=request.user, imagen=form.cleaned_data["imagen"])
            avatar.save()
            return render(request, 'blog/inicio.html', {'usuario':request.user,"mensaje":f"El avatar se agrego exitosamente.",'imagen':obtenerAvatar(request)})
    else:
        form = AvatarForm()
    return render(request, "blog/agregaravatar.html", {"form": form,'usuario':request.user,'imagen':obtenerAvatar(request)})

def obtenerAvatar(request):
    lista=Avatar.objects.filter(user=request.user)
    if len(lista)!=0:
        imagen=lista[0].imagen.url
    else:
        imagen="no hay avatar"
    return imagen

@login_required
def crear_publicacion(request):
    usuario=request.user
    if request.method == "POST":
        publicacion = CrearPublicacion(request.POST, request.FILES)
        if publicacion.is_valid():
            informacion = publicacion.cleaned_data
            publicacion = Publicacion(imagen=informacion["imagen"], nombre=informacion["nombre"], categoria=informacion["categoria"], descripcion=informacion["descripcion"], fecha=datetime.today(), autor=usuario)
            publicacion.save()
            return render(request, "blog/inicio.html", {"mensaje":f"La publicacion se ha realizado correctamente.",'imagen':obtenerAvatar(request)})
    else:
        publicacion = CrearPublicacion()
        imagen=Avatar
        return render (request, "blog/crearpublicacion.html", {'publicacion': publicacion,'imagen':obtenerAvatar(request)})

@login_required 
def listarpublicaciones(request):
    listarpublicaciones=Publicacion.objects.all()
    return render (request, 'blog/listarpublicaciones.html', {'listarpublicaciones': listarpublicaciones,'imagen':obtenerAvatar(request)})


def leerpublicacion(request, id):
    leerpublicacion=Publicacion.objects.get(id=id)
    return render (request, 'blog/leerpublicacion.html', {'leerpublicacion': leerpublicacion})

def about(request):
    return render (request, 'blog/about.html')
    
@login_required
def editarpublicacion(request, id):
    if(comprobacion(request) == True):
        publicacion = Publicacion.objects.get(id=id)
        if request.method == "POST":
            form = CrearPublicacion(request.POST, request.FILES)
            if form.is_valid():
                info = form.cleaned_data
                publicacion.imagen = info["imagen"]
                publicacion.nombre = info["nombre"]
                publicacion.categoria = info["categoria"]
                publicacion.descripcion = info["descripcion"]
                publicacion.save()
            
                return render(request, "blog/inicio.html", {'mensaje': f"la publicacion se ha realizado correctamente"})
        else:
            form = CrearPublicacion(initial ={"imagen":publicacion.imagen, "nombre":publicacion.nombre, "categoria":publicacion.categoria, "descripcion":publicacion.descripcion})
        return render (request, "blog/editarpublicacion.html", {"formulario":form, "id":publicacion.id,'imagen':obtenerAvatar(request)})
    else:
        return render(request, "blog/inicio.html", {'mensaje': 'El usuario no tiene permitido editar','imagen':obtenerAvatar(request)}) 

@login_required
def deletepublicacion(request, id):
    if(comprobacion(request) == True):
        publicaciones = Publicacion.objects.get(id=id)
        publicaciones.delete()
        listarpublicaciones=Publicacion.objects.all()
        return render(request, "blog/listarpublicaciones.html", {'listarpublicaciones': listarpublicaciones,'imagen':obtenerAvatar(request)}) 
    else:
        return render(request, "blog/inicio.html", {'mensaje': 'El usuario no tiene permitido eliminar','imagen':obtenerAvatar(request)}) 

#trabaja como funcion
def comprobacion(request):
    if((str(request.user)=="admin")):
        usuario=True
    else:
        usuario=False
    return usuario

@login_required
def perfil(request):
    user=request.user
    if request.method == "POST":
        form = Perfil(request.POST, request.FILES)
        if form.is_valid(): 
            informacion = form.cleaned_data
            user.descripcion=informacion["descripcion"]
            user.link=informacion["link"]
            user.imagen=informacion["imagen"]
            user.save()
            return render(request,'blog/inicio.html', {"mensaje":f"Se agrego informacion correctamente",'imagen':obtenerAvatar(request)})
    else:
        form = Perfil()
    return render(request, "blog/agregarinformacion.html", {"form": form,'usuario':request.user,'imagen':obtenerAvatar(request)})

def miperfil(request):
    miperfil=Perfil.objects.all() 
    return render (request, 'blog/miperfil.html', {'miperfil': miperfil,'imagen':obtenerAvatar(request)})