# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class CiaaR1(models.Model):
    id_ciaa = models.AutoField(db_column='id_CIAA', primary_key=True)  # Field name made lowercase.
    cliente = models.CharField(db_column='Cliente', max_length=255)  # Field name made lowercase.
    orden = models.CharField(db_column='Orden', max_length=255)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=255)  # Field name made lowercase.
    puesto = models.CharField(db_column='Puesto', max_length=255)  # Field name made lowercase.
    fecha = models.CharField(db_column='Fecha', max_length=255)  # Field name made lowercase.
    entrada = models.CharField(db_column='Entrada', max_length=255)  # Field name made lowercase.
    salida = models.CharField(db_column='Salida', max_length=255)  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=255)  # Field name made lowercase.
    geolocalizacion = models.CharField(db_column='Geolocalizacion', max_length=255)  # Field name made lowercase.
    foto = models.CharField(db_column='Foto', max_length=255)  # Field name made lowercase.
    codigo = models.CharField(db_column='Codigo', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CIAA_R1'

