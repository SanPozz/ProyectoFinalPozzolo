#URLS de la APP para coordinar con el URSL.py del proyecto.
#Informo con formato path('nombre de clase/', clase)

from django.urls import path
from blog.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', inicio, name='inicio'),
    path('login/', login_request, name='login'),
    path('registro/',registro, name='registro'),
    path('editarPerfil/', editarPerfil, name='editarperfil'),
    path('logout/', LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('editarPerfil/agregar_avatar', agregar_avatar, name='agregaravatar'),
    path('editarPerfil/agregarinformacion', perfil, name='agregarinformacion'),
    path('miperfil/', miperfil, name='miperfil'),
    path('listarpublicaciones/', listarpublicaciones, name = 'listarpublicaciones'),   
    path('crearpublicacion/', crear_publicacion, name = 'crearpublicacion'),
    path('editarpublicacion/<id>', editarpublicacion, name = 'editarpublicacion'),
    path('deletepublicacion/<id>', deletepublicacion, name='eliminarpublicacion'),
    path('leerpublicacion/<id>', leerpublicacion, name = 'leerpublicacion'),
    path('about/', about, name ='about'),

    ]

