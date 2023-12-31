# Generated by Django 4.2.1 on 2023-05-30 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='perro',
            name='id_usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='libretavacunas',
            name='perro',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='LibretaVacunas', to='mascotas.perro'),
        ),
        migrations.AddField(
            model_name='historiaclinica',
            name='perro',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='HistoriaClinica', to='mascotas.perro'),
        ),
    ]
