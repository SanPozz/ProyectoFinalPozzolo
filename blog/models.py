from django.db import models
from django.contrib.auth.models import User    
from ckeditor.fields import *

class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    descripcion = RichTextField(blank=True, null=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    imagen = models.ImageField(upload_to='imagen', null=True, blank=True)

    def __str__(self):
        return self.user.first_name


class Publicacion(models.Model):
    nombre=models.CharField(max_length=30)
    categoria=models.CharField(max_length=15)
    descripcion=models.CharField(max_length=500, blank=True, null=True)
    fecha=models.DateField(auto_now_add=True)
    autor=models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    imagen = models.ImageField(upload_to='imagen', null=True, blank=True)
    class Meta:
        verbose_name_plural = "Publicaciones"

    def __str__(self):
        return self.nombre