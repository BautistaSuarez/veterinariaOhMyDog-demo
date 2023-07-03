from django.db import models
from apps.users.models import CustomUser

class Turno (models.Model):
    TIME_CHOICES = (
        ('M', 'Mañana',),
        ('T', 'Tarde',),
    )
    Fecha =  models.DateField(auto_now=False, auto_now_add=False)
    Franja_Horaria  = models.TextField(
        max_length=1,
        choices=TIME_CHOICES,
    )
    Pendiente = models.BooleanField(default=False)
    Descripcion = models.TextField()
    id_usuario = models.ForeignKey( 
        CustomUser, on_delete=models.CASCADE, null=True, blank=True)
