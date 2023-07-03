from django.db import models

class Colecta(models.Model):

        def __str__(self):
                return self.titulo

        titulo = models.CharField(max_length=100)
        descripcion = models.TextField()
        monto_meta = models.FloatField()
        monto_recaudado = models.FloatField(default=0)
        fecha_limite = models.DateField(auto_now=False, auto_now_add=False)
        concluida = models.BooleanField(default=False)
