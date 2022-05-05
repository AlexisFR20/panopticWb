from django.db import models
from core.models import Cliente, User
import datetime


# Create your models here.
class TipoIncidente(models.Model):    
    nombre = models.CharField(max_length=30, verbose_name="Nombre")
    alias  = models.CharField(max_length=30, verbose_name="Alias")
    icono  = models.ImageField(upload_to='tipo_incidentes_iconos')
    
    def __unicode__(self):
        return unicode(self.nombre, 'utf-8')

class Incidente(models.Model):
    TIPO = (
        ("asalto_transeuntes", "Asalto a transeuntes"),
        ("asalto_negocio", "Asalto a negocio"),
        ("casa_habitacion", "Casa habitacion"), 
        ("homicidio", "Homicidio"), 
        ("secuestro", "Secuestro"), 
        ("carjacking", "Carjacking"),
        ("autopartes", "Autopartes"),
        ("hotel", "Hotel"),
        ("aeropuerto", "Aeropuerto"),
    )
    tipo        = models.CharField(max_length=30, choices=TIPO, verbose_name="Tipo")
    tipor       = models.ForeignKey(TipoIncidente, on_delete=models.SET_NULL, blank=True, null=True)
    fecha       = models.DateField()
    hora        = models.TimeField(default='07:00')
    titulo      = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(max_length=3000, blank=True, null=True)
    #ubicacion  = models.CharField(max_length=150, blank=True, default='', verbose_name="Ubicación")
    direccion   = models.CharField(max_length=150, blank=True, null=True)
    pais        = models.CharField(max_length=30, blank=True, null=True)
    ciudad      = models.CharField(max_length=30, blank=True, null=True)
    estado      = models.CharField(max_length=30, blank=True, null=True)    
    lat         = models.FloatField(blank=True, default=0, verbose_name="Latitud (coordenada)")
    lng         = models.FloatField(blank=True, default=0, verbose_name="Longitud (coordenada)")
    url_noticia = models.TextField(blank=True, null=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    label       = models.CharField(max_length=150, blank=True, null=True)
    cantidad    = models.IntegerField(default=1)
    nivel       = models.IntegerField(default=1)

    def __str__(self):
        return self.tipo

class Alarma(models.Model):
    ESTATUS = (
        ("relevante", "RELEVANTE"),
        ("normal", "NORMAL"),
        ("pendiente", "PENDIENTE")
    )    
    incidente    = models.ForeignKey(Incidente, on_delete=models.SET_NULL, blank=True, null=True)
    usuario      = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    cliente      = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    nombre       = models.CharField('Nombre', max_length=30)
    tipo         = models.CharField('Tipo', max_length=30, default='')
    estatus      = models.CharField('Estatus de Alarma', max_length=30, choices=ESTATUS, default='normal')      
    accion       = models.TextField(verbose_name="Acción", default='')
    fecha_inicio = models.DateField('Fecha de Inicio', default=datetime.date.today)
    hora_inicio  = models.TimeField(default='7:00')
    fecha_fin    = models.DateField('Fecha Fin', default=datetime.date.today)
    hora_fin     = models.TimeField(default='7:00')
    url          = models.TextField(blank=True, default='')
    
    def __str__(self):
        return self.nombre
        
