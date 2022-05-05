from django.db import models
from django.utils.timezone import now
from pymysql import NULL
from core.models import User, Planta, Role, Cliente
import os
from django_cryptography.fields import encrypt
from django.conf import settings
from decimal import *
#Modelo de Predictive Analytics
    

# Create your models here.
#class Analisis(models.Model):
#    nombre = models.CharField(max_length=100)
#
#    def __str__(self):
#        return str(self.nombre)

class Categoria_Encuesta(models.Model):
    nombre = models.CharField('Nombre de Categoria Encuesta', max_length=50)
    #analisis = models.ForeignKey(Analisis, on_delete=models.SET_NULL, blank=True, null=True)
    icono = models.ImageField('Icono', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Encuesta(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    categoria = models.ForeignKey(Categoria_Encuesta, on_delete=models.SET_NULL, blank=True, null=True)
    path_encuesta = models.TextField('Ruta', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Pregunta(models.Model):
    pregunta = models.TextField()
    valor = models.IntegerField(default=10)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    req_evidencia = models.BooleanField(default=False)
    orden = models.IntegerField(default=1)

    class Meta:
        ordering = ["orden"]
        verbose_name_plural = "Preguntas"

    def __str__(self):
        return str(self.encuesta)+": "+str(self.pregunta)

class Papeleta(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    user_aguilas = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_aguilas")
    contacto_operativo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacto_operativo", blank=True, null=True)
    contacto_logistica = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacto_logistica", blank=True, null=True)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    evidencia = models.BooleanField(default=False)

    def __str__(self):
        return str(self.encuesta)+": "+str(self.fecha)

    def calcularRiesgo(self):
        riesgo = 0
        
        respuestas = self.respuestas.all()
        for r in respuestas:
            print("calculado "+str(riesgo)+" + "+str(r.calcularRiesgo())+" = "+str( Decimal(str(riesgo)) + Decimal( str(r.calcularRiesgo()) )))
            riesgo += Decimal( str(r.calcularRiesgo()))
        print("Riesgo papeleta "+str(riesgo))
        return riesgo

    def calcularVulnerabilidad(self):
        vulnerable = 0
        total = 0
        respuestas = self.respuestas.all()
        for r in respuestas:
            total += 1
            if(r.respuesta == 0  and r.calcularRiesgo() > 0):
                vulnerable += 1

        if total == 0:
            return 0
        return vulnerable/total*100
    
    def fecha_corta(self):
        return self.fecha.strftime("%Y-%m-%d, %I:%M %p")

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, blank=True, null=True)
    pregunta_text = models.TextField()
    valor = models.IntegerField(default=10)
    respuesta = models.IntegerField()
    cumple = models.IntegerField()
    ocurrencia = models.IntegerField()
    impacto = models.IntegerField()
    resultado = models.IntegerField()
    requiere_evidencia = models.BooleanField(default=False)#guarda segun lo estipule la pregunta
    observacion = models.TextField()
    papeleta = models.ForeignKey(Papeleta, on_delete=models.CASCADE, related_name="respuestas")

    def __str__(self):
        return str(self.pregunta)+": "+str(Respuesta)
        
        
    def calcularRiesgo(self):
        riesgo = ((self.ocurrencia*self.impacto)/25*self.valor)
        #print("antes de recomendacion "+str(riesgo))
        for rec in self.recomendacion_set.all():
            if rec.status == "cerrado":
                #print("riesgo = "+str(riesgo)+" - "+str(rec.ponderacion))
                riesgo = Decimal(str(riesgo)) - Decimal( str(rec.ponderacion) )

        #print("despues de recomendacion "+str(riesgo))
        return riesgo
        
    def gallery(self):
        print("evidencia "+str(self.papeleta_id)+"/"+str(self.pregunta_id))
        print(settings.BASE_DIR)
        path=os.path.join(settings.BASE_DIR, 'media/evidencia/papeletas/'+str(self.papeleta_id)+'/'+str(self.pregunta_id))
        print("path "+str(path))
        if os.path.exists(path):
            img_list = os.listdir(path)   
            return img_list
        return ""

class Recomendacion(models.Model): 
    STATUS = (
        ("en_proceso", "En proceso"),
        ("vencido", "Vencido"),
        ("cerrado", "Cerrado"), 
        ("cancelado", "Cancelado")
    )
    
    #Aplicable a las respuesta con NO
    papeleta = models.ForeignKey(Papeleta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE, blank=True, null=True)
    nombre = models.CharField('Nombre', max_length=100)
    descripcion = models.TextField('Descripción')
    ponderacion = models.FloatField('Ponderación')#porcentaje
    vulnerabilidad = models.IntegerField('Vulnerabilidad', default=10)
    costo = models.BooleanField('Costo', default=False)
    evidencia = models.FileField('Evidencia', upload_to='evidencia/recoemdaciones/%Y/%m/%d/', blank=True, null=True)
    fecha_compromiso = models.DateField('Fecha Compromiso', blank=True, null=True)
    user_responsable = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_responsable", blank=True, null=True)
    #Editor - Persona de Aguilas
    user_aguilas = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="recomendacion_user_aguilas", blank=True, null=True)
    status = models.CharField('Estatus', max_length=100, choices=STATUS, default="en_proceso")
    area = models.ForeignKey(Categoria_Encuesta, on_delete=models.SET_NULL, blank=True, null=True)#se puede obtener de la papeleta

class EvidenciaRecomendacion(models.Model):
    recomendacion = models.ForeignKey(Recomendacion, on_delete=models.CASCADE)
    foto = models.ImageField('Foto', blank=True, null=True)
    documento = models.FileField('Documento', blank=True, null=True)
    nota = models.TextField('Nota')

    def __str__(self):
        return str(self.recomendacion)

#Para remover
class Area(models.Model):
    nombre = models.CharField('Área', max_length=100)
    icono  = models.ImageField('Icono', blank=True, null=True)

class Segmento(models.Model):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField('Segmento', max_length=100)    
