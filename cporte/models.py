from statistics import mode
from django.db import models
from django.core.validators import FileExtensionValidator
import os

# Create your models here.
class PorteCliente(models.Model):
    REGIMEN_CHOICES = (
        ("601", "601 - General de Ley Personas Morales"),
        ("603", "603 - Personas Morales con Fines no Lucrativos"),
        ("609", "609 - Consolidación"),
        ("612", "612 - Personas Fisicas con Actividades Empresariales y Profesionales"),
        ("620", "620 - Sociedades Cooperativas de Producción que optan por diferir sus ingresos"),
        ("622", "622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras"),
        ("632", "623 - Opcional para Grupos de Sociedades"),
        ("624", "624 - Coordinados"),
        ("628", "628 - Hidrocarburos"),
        ("607", "607 - Régimen de Enajenación o Adquisición de Bienes")
    )

    #No se usa, pero django lo necesita para el historial de migraciones
    def upload_photo_to(self, filename):
        nombre = self.nombre.replace(" ","_")
        type = filename.split(".")
        dir_file = ("carta_porte/" + nombre + "/" + type[1] + "/" + filename)
        return os.path.join(dir_file)
    
    def upload_logo_to(self, filename):
        nombre = self.nombre.replace(" ","_")
        dir_file = ("carta_porte/" + nombre + "/img/" + filename)
        return os.path.join(dir_file)

    nombre = models.CharField(max_length = 100)
    rfc = models.CharField(max_length = 100)
    razon_social = models.CharField(max_length = 100) 
    regimen_fiscal = models.CharField(max_length=3, choices=REGIMEN_CHOICES)
    calle = models.CharField(max_length=50, default='')
    exterior = models.CharField(max_length=10, default='')
    interior = models.CharField(max_length=10, default='')
    colonia =  models.CharField(max_length=50, default='')
    cp = models.CharField(max_length=5, default='')
    localidad = models.CharField(max_length=20, default='')
    municipio = models.CharField(max_length=20, default='')
    estado = models.CharField(max_length=20, default='')
    pais = models.CharField(max_length=20, default='')
    tipoPermiso = models.CharField(max_length=20, blank=True, null=True)
    numPermiso = models.CharField(max_length=30, blank=True, null=True)
    #path_privateKey = models.CharField(max_length=100, default = '')
    #path_key = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['key'])])
    #path_cer = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['cer'])])
    path_img = models.FileField(upload_to = upload_logo_to, validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])], default='')

    def __str__(self):
        return self.nombre

class PorteReceiver(models.Model):

    #No se usa, pero django necesita esta función para el historial de migraciones.
    def upload_photo_to(self, filename):
        nombre = self.nombre.replace(" ","_")
        type = filename.split(".")
        dir_file = ("carta_porte/" + self.porteCliente.nombre + "/receivers/" + nombre + "/" + type[1] + "/" + filename)
        return os.path.join(dir_file)

    porteCliente = models.ForeignKey(PorteCliente, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length = 100)
    rfc = models.CharField(max_length = 100)
    razon_social = models.CharField(max_length = 100)
    calle = models.CharField(max_length=50, default='')
    exterior = models.CharField(max_length=10, default='')
    interior = models.CharField(max_length=10, default='')
    colonia =  models.CharField(max_length=50, default='')
    cp = models.CharField(max_length=5, default='')
    localidad = models.CharField(max_length=20, default='')
    municipio = models.CharField(max_length=20, default='')
    estado = models.CharField(max_length=20, default='')
    pais = models.CharField(max_length=20, default='')
    #path_privateKey = models.CharField(max_length=100, default = '')
    #path_key = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['key'])])
    #path_cer = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['cer'])])

    def __str__(self):
        return self.nombre


class PorteCarta(models.Model):
    json = models.JSONField()
    PorteReceiver = models.ForeignKey(PorteReceiver, on_delete=models.SET_NULL, blank=True, null=True)
    figura = models.CharField(max_length = 50)
    origen = models.CharField(max_length = 100)
    destino = models.CharField(max_length = 100)
    status = models.IntegerField(default=0)
    pdf = models.TextField(blank = True, null = True)

class PorteFigura(models.Model):
    porteCliente = models.ForeignKey(PorteCliente, on_delete=models.SET_NULL, blank=True, null=True)
    tipo = models.CharField(max_length=10)
    rfc = models.CharField(max_length=13)
    nombre = models.CharField(max_length=30)
    licencia = models.CharField(max_length=30)
    pais = models.CharField(max_length=10, blank=True, null=True)
    cp = models.CharField(max_length=6)
    estado = models.CharField(max_length=15)
    municipio = models.CharField(max_length=20)
    colonia = models.CharField(max_length=20)
    calle = models.CharField(max_length=20)
    ext = models.CharField(max_length=10)
    int = models.CharField(max_length=10)
    referencia = models.CharField(max_length=20)


class Seguro(models.Model):
    porteCliente = models.ForeignKey(PorteCliente, on_delete=models.SET_NULL, blank=True, null=True)
    aseguradora = models.CharField(max_length=20)
    poliza = models.CharField(max_length=20)

class Autotransporte(models.Model):
    porteCliente = models.ForeignKey(PorteCliente, on_delete=models.SET_NULL, blank=True, null=True)
    #permsct = models.CharField(max_length=5)
    #numpermsct = models.CharField(max_length=30)
    tipoTransporte = models.CharField(max_length=10)
    placas = models.CharField(max_length=20)
    anio = models.CharField(max_length=4)
