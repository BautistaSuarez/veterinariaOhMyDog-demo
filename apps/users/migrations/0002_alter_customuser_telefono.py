# Generated by Django 4.2.1 on 2023-05-31 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='telefono',
            field=models.IntegerField(verbose_name='telefono'),
        ),
    ]
