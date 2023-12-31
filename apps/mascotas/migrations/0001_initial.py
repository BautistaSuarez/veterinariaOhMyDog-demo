# Generated by Django 4.2.1 on 2023-05-30 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriaClinica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LibretaVacunas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('marca', models.CharField(max_length=100)),
                ('tipo', models.CharField(max_length=100)),
                ('lote', models.CharField(max_length=100)),
                ('numero_dosis', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Perro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('raza', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('sexo', models.CharField(choices=[('H', 'Hembra'), ('M', 'Macho')], max_length=1)),
                ('castrado', models.BooleanField()),
            ],
        ),
    ]
