from django.db import models
from core.models import User
from django_resized import ResizedImageField
import mimetypes
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from core.models import User, Planta, Role, Cliente, Sucursal, Region
from datetime import datetime, timedelta

# Create your models here

class CategoriaRondin(models.Model):
    nombre = models.CharField(max_length=100)

class Rondin(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
    planta = models.ForeignKey(Planta, on_delete = models.CASCADE)
    categoria = models.ForeignKey(CategoriaRondin, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=50, default = "nombre rondin")
    tiempo_estimado = models.IntegerField(verbose_name="Tiempo estimado (minutos)")#tiempo estimado en minutos
    correos_contacto = models.TextField(verbose_name="Correos de contacto (separar por coma)")#separar correos por coma
    admin_aguilas = models.ForeignKey(User, verbose_name="Creado por", on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(verbose_name="Ã‚Â¿Activo?", default=True)
    #autogenerar qr del rondin
    class Meta:
        verbose_name_plural = "Rondines"

class Punto(models.Model):
    rondin = models.ForeignKey(Rondin, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    tareas = models.TextField()#separadas por coma
    lat = models.FloatField(blank=True, default=0, verbose_name="Latitud (coordenada)")
    lng = models.FloatField(blank=True, default=0, verbose_name="Longitud (coordenada)")
    orden = models.IntegerField(verbose_name="Orden", default=0)
    activo = models.BooleanField(verbose_name="Ã‚Â¿Activo?", default=True)
    #generar qr del punto    

    def get_list_tareas(self):
        return self.tareas.split(",")
        
    class Meta:
        ordering = ['orden']
    

class RondinHecho(models.Model):
    rondin      = models.ForeignKey(Rondin, on_delete=models.CASCADE, related_name='rondin_rondinhecho')
    hora_inicio = models.DateTimeField() 
    hora_fin    = models.DateTimeField(blank=True, null=True)
    guardia     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def r_hora_inicio(self):
        return self.hora_inicio.strftime("%m/%d, %I:%M %p")
    
    def r_hora_fin(self):
        return self.hora_fin.strftime("%m/%d, %I:%M %p")

    def rs_hora_inicio(self):
        return self.hora_inicio.strftime("%Y-%m-%d")

class PuntoHecho(models.Model):
    rondinhecho = models.ForeignKey(RondinHecho, on_delete=models.CASCADE)
    punto       = models.ForeignKey(Punto, on_delete=models.CASCADE, default=1)
    hora_inicio = models.DateTimeField() 
    hora_fin    = models.DateTimeField(blank=True, null=True)
    
    def ph_hora_inicio(self):
        return self.hora_inicio.strftime("%m/%d, %I:%M %p")
    
    def ph_hora_fin(self):
        if not self.hora_fin:
            return 'En progreso'
        return self.hora_fin.strftime("%m/%d, %I:%M %p") 

class EvidenciaPunto(models.Model):
    rondinhecho = models.ForeignKey(RondinHecho, on_delete=models.CASCADE, default=1)
    punto = models.ForeignKey(Punto, on_delete=models.CASCADE, default=1)
    nota = models.TextField()
    evidencia = models.FileField(upload_to='evidencia/rondines/%Y/%d/%m/', null=True)

    def tipo(self):
        file_type, file_encoding = mimetypes.guess_type(self.evidencia.url)
        #print(file_type)
        return file_type

#Modelo de previsitantes
"""
class F_PreVisitantes(models.Model):
    nombre = models.CharField(max_length = 100)
    planta = models.ForeignKey(Planta, on_delete = models.SET_NULL, null=True,related_name="planta_fprevisitante")
    anfitrion = models.CharField(max_length = 100)
    fecha_registro = models.DateTimeField(default=now, blank=True, null=True)
    fecha_agendada = models.DateField(blank = True, null = True)
    qr_url = models.CharField(max_length = 150, null = True, blank=True)
    status = models.IntegerField(default=0)
"""

class F_Visitantes(models.Model):
    CONFIRM = (
        (True, "Si"),
        (False, "No")
    )

    TIPO = (
        ("visitante", "Visitante"),
        ("proveedores", "Proveedor"),
        ("contratistas", "Contratista")
    )
    
    planta             = models.ForeignKey(Planta, on_delete = models.SET_NULL, null = True, related_name="planta_fvisitante")
    tipo               = models.CharField(choices=TIPO, max_length=20, default="visitante") 
    nombre             = models.CharField(max_length       = 50)    
    empresa            = models.CharField(max_length       = 100)
    anfitrion          = models.CharField(max_length       = 50)
    confirmo_anfitrion = models.BooleanField(choices       = CONFIRM, default="")
    identificacion     = models.CharField(max_length       = 100, blank = True, verbose_name = "# y tipo de indentificacion")
    ine_frontal        = models.FileField(upload_to='fotos_visitantes/ine_frontal/%Y/%d/%m/', blank=True, null=True)   
    ine_posterior      = models.FileField(upload_to='fotos_visitantes/ine_posterior/%Y/%d/%m/', blank=True, null=True)
    gafete             = models.CharField(max_length       = 100, blank = True, null=True)
    placas             = models.CharField(max_length       = 10, blank  = True)
    entrada            = models.DateTimeField(blank=True, null=True)
    salida = models.DateTimeField(blank=True, null=True) 
    #email = models.EmailField('E-mail', blank=True, null=True, max_length=254)
    #telefono = models.CharField('Teléfono', blank=True, null=True, max_length=128, default='')    
    #contacto = models.CharField('Posición', blank=True, null=True, max_length=128, default='')
    #domicilio = models.CharField('Domicilio', blank=True, null=True, max_length=100)
    #foto = ResizedImageField('Foto', upload_to='avatars', blank=True, null=True, size=[1024, 1024], force_format='JPEG', quality=65)
    pre = models.IntegerField(default=0)
    qr_url = models.CharField(max_length = 150, blank=True, null=True)
    fecha_agendada = models.DateField(blank=True,null=True)
    pre_status = models.IntegerField(default=0)

    def entradaformateada(self):        
        return self.entrada.strftime("%m/%d, %I:%M %p")
        
    def salidaformateada(self):
        if not self.salida:
            return 'No ha salido.'
        return self.salida.strftime("%m/%d, %I:%M %p") 

class F_ES_Trailers(models.Model):
    
    entrada                 = models.DateTimeField(auto_now = False, blank=True, null=True)
    salida                  = models.DateTimeField(auto_now = False, blank=True, null=True)
    origen                  = models.TextField(blank = True)
    destino                 = models.TextField(blank = True)
    nombre_chofer           = models.CharField(max_length       = 50, blank = True)
    transportista           = models.CharField(max_length       = 100, blank = True)
    placas                  = models.CharField(max_length       = 10, blank = True)
    caja                    = models.CharField(max_length       = 10, blank = True)
    factura_remision_ip     = models.CharField(max_length       = 20, blank = True)
    n_sello                 = models.CharField(max_length       = 20, blank = True)
    contenido_caja          = models.TextField(blank = True)
    autoriza                = models.CharField(max_length       = 50, blank = True)
    firma_chofer            = models.FileField(upload_to='festrilers/firmas/chofer/%Y/%d/%m/', blank=True, null=True) 
    n_licencia              = models.CharField(max_length       = 20, blank = True)
    firma_oficial_seguridad = models.FileField(upload_to='festrilers/firmas/guardia/%Y/%d/%m/', blank=True, null=True)
    planta                  = models.ForeignKey(Planta, on_delete = models.SET_NULL, null = True)
    notas                   = models.TextField(default="")
    pedimento_caja          = models.FileField(upload_to='festrilers/documentos/pedimento/%Y/%d/%m/', blank=True, null=True)
    bill_caja               = models.FileField(upload_to='festrilers/documentos/bill/%Y/%d/%m/', blank=True, null=True)
    factura_caja            = models.FileField(upload_to='festrilers/documentos/factura/%Y/%d/%m/', blank=True, null=True)
    ine_chofer              = models.FileField(upload_to='festrilers/documentos/ine/%Y/%d/%m/', blank=True, null=True)
    cajon_id                = models.CharField(max_length       = 10, blank = True, null=True)

class F_18_puntos_Trailer(models.Model):

    RESULT_A = (
        (0, "No"),
        (1, "Si")
    )

    RESULT_B = (
        (0, "No"),
        (1, "Si"),
        (2, "NA")
    )

    planta = models.ForeignKey(Planta, on_delete = models.SET_NULL, null = True)
    inspecionado_por = models.ForeignKey(User, verbose_name="Inspeccionado por", on_delete=models.SET_NULL, null=True, blank=True)

    fecha = models.DateTimeField(auto_now_add = True)
    n_contenedor = models.CharField(max_length = 20, default="")
    placas_contenedor = models.CharField(max_length = 20, default="")
    n_economico = models.CharField(max_length = 20, default="")
    placas_tractocamion = models.CharField(max_length = 20, default="")
    nombre_chofer = models.CharField(max_length = 50, default="")
    vigencia_licencia = models.CharField(max_length = 50, default="")
    transportista = models.CharField(max_length = 50)
    n_sello = models.CharField(max_length = 20)
    
    defensa = models.IntegerField(default = 1, choices = RESULT_A)
    nota_defensa = models.TextField(default="")
    evidencia_defensa = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    motor = models.IntegerField(default = 1, choices = RESULT_A)
    nota_motor = models.TextField(default="")
    evidencia_motor = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None) 

    llantas = models.IntegerField(default = 1, choices = RESULT_A)
    nota_llantas = models.TextField(default="")
    evidencia_llantas = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    piso_cabina = models.IntegerField(default         = 1, choices            = RESULT_A)
    nota_piso_cabina = models.TextField(default="")
    evidencia_piso_cabina = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    tanque_conbustible = models.IntegerField(default         = 1, choices            = RESULT_A)
    nota_tanque_conbustible = models.TextField(default="")
    evidencia_tanque_conbustible = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    cabina = models.IntegerField(default = 1, choices = RESULT_A)
    nota_cabina = models.TextField(default="")
    evidencia_cabina = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    suspension_aire = models.IntegerField(default = 1, choices = RESULT_A)
    nota_suspension_aire = models.TextField(default="")
    evidencia_suspension_aire = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    flecha_embrague = models.IntegerField(default = 1, choices = RESULT_A)
    nota_flecha_embrague = models.TextField(default="")
    evidencia_flecha_embrague = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)
    
    quinta_rueda = models.IntegerField(default = 1, choices = RESULT_A)
    nota_quinta_rueda = models.TextField(default="")
    evidencia_quinta_rueda = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    debajo_plataforma = models.IntegerField(default = 1, choices = RESULT_B)
    nota_debajo_plataforma = models.TextField(default="")
    evidencia_debajo_plataforma = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    puertas_internas_externas = models.IntegerField(default = 1, choices = RESULT_B)
    nota_puertas_internas_externas = models.TextField(default="")
    evidencia_puertas_internas_externas = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    piso_interior_cajas = models.IntegerField(default = 1, choices = RESULT_B)
    nota_piso_interior_cajas = models.TextField(default="")
    evidencia_piso_interior_cajas = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    paredes_laterales = models.IntegerField(default = 1, choices = RESULT_B)
    nota_paredes_laterales = models.TextField(default="")
    evidencia_paredes_laterales = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    pared_frontal = models.IntegerField(default = 1, choices = RESULT_B)
    nota_pared_frontal = models.TextField(default="")
    evidencia_pared_frontal = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)
     
    techo = models.IntegerField(default = 1, choices = RESULT_B)
    nota_techo = models.TextField(default="")
    evidencia_techo = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)
    
    unidad_refrigeracion = models.IntegerField(default = 1, choices = RESULT_B)
    nota_unidad_refrigeracion = models.TextField(default="")
    evidencia_unidad_refrigeracion = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    escape = models.IntegerField(default = 1, choices = RESULT_B)
    nota_escape = models.TextField(default="")
    evidencia_escape = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None)

    #Debe cumplir los requisitos de ver verificar, jalar y torcer para poder marcar el siguiente PUNTO CRITICO
    revision_sello = models.IntegerField(default = 1, choices = RESULT_B)
    nota_revision_sello = models.TextField(default="")
    evidencia_revision_sello = models.FileField(upload_to='evidencia/revision18puntos/%Y/%d/%m/', blank=True, null=True, default=None) 
    
    def p18_fecha(self):
        return self.fecha.strftime("%m/%d %Y, %I:%M %p")

    def qtyEvidence(self):
        #Regresa la cantidad de evidencias encontradas en el registro en particular 
        result = 0
        if self.evidencia_defensa:
            result += 1      
        if self.evidencia_motor:
            result += 1
        if self.evidencia_llantas:
            result += 1
        if self.evidencia_piso_cabina:
            result += 1
        if self.evidencia_tanque_conbustible:
            result += 1
        if self.evidencia_cabina:
            result += 1
        if self.evidencia_suspension_aire:
            result += 1
        if self.evidencia_flecha_embrague:
            result += 1
        if self.evidencia_quinta_rueda:
            result += 1
        if self.evidencia_debajo_plataforma:
            result += 1
        if self.evidencia_puertas_internas_externas:
            result += 1
        if self.evidencia_piso_interior_cajas:
            result += 1
        if self.evidencia_paredes_laterales:
            result += 1
        if self.evidencia_pared_frontal:
            result += 1
        if self.evidencia_techo:
            result += 1
        if self.evidencia_unidad_refrigeracion:
            result += 1
        if self.evidencia_escape:
            result += 1
        if self.evidencia_revision_sello:
            result += 1         
        
        return result

    def onEvidence(self):
        #Regresa valor verdadero si se encuentra evidencia en cualquier de los puntos que se han revisado 
        result = False
        if self.evidencia_defensa or self.evidencia_motor or self.evidencia_llantas or self.evidencia_piso_cabina or self.evidencia_tanque_conbustible or self.evidencia_cabina or self.evidencia_suspension_aire or self.evidencia_flecha_embrague or self.evidencia_quinta_rueda or self.evidencia_debajo_plataforma or self.evidencia_puertas_internas_externas or self.evidencia_piso_interior_cajas or self.evidencia_paredes_laterales or self.evidencia_pared_frontal or self.evidencia_techo or self.evidencia_unidad_refrigeracion or self.evidencia_escape or self.evidencia_revision_sello:
            result = True
        
        return result

class Vacante(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.SET_NULL, null=True)
    n_vacantes = models.IntegerField('# vacantes', default=1)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateField("Fecha", default=now)
    observaciones = models.TextField('Observaciones', default='')

class Rotacion(models.Model):
    TURNO = (
        ("dia", "Dia"),
        ("noche", "Noche")
    )

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50)
    motivo = models.TextField(default="")
    turno = models.CharField(max_length=50, choices=TURNO, default="dia")
    
class Incidentes(models.Model):
    STATUS = (
        ("abierto", "Abierto"),
        ("revision", "Revision"),
        ("progreso", "Progreso"),
        ("cerrado", "Cerrado")
    )

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    guardia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nota = models.TextField(default="")
    evidencia = models.FileField(upload_to='evidencia/incidencias/%Y/%d/%m/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS, default="abierto")
    acciones_tomadas = models.TextField(default="")

    def tipo(self):
        file_type, file_encoding = mimetypes.guess_type(self.evidencia.url)
        print(file_type)
        return file_type

    def fechaformateada(self):
        return self.fecha.strftime("%m/%d %Y, %I:%M %p")

class IncidenciasServicio(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    incidencia = models.TextField()
    acciones_tomadas = models.TextField()
    
class EntradaEquipo(models.Model):
    visitante = models.ForeignKey(F_Visitantes, on_delete=models.CASCADE, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    guardia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def fechaformateada(self):
        return self.fecha.strftime("%m/%d %Y, %I:%M %p")

class EntradaMateriales(models.Model):
    visitante = models.ForeignKey(F_Visitantes, on_delete=models.CASCADE, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    guardia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100)

    def fechaformateada(self):
        return self.fecha.strftime("%m/%d %Y, %I:%M %p")

class ItemEntradaEquipo(models.Model):
    entradaequipo = models.ForeignKey(EntradaEquipo, on_delete=models.CASCADE, null=True, blank=True, related_name="item")
    descripcion = models.CharField(max_length=100)
    n_serie = models.CharField(max_length=50)
    cantidad = models.IntegerField()

class ItemEntradaMaterial(models.Model):
    entradamateriales = models.ForeignKey(EntradaMateriales, on_delete=models.CASCADE, null=True, blank=True, related_name="item")
    descripcion = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)

class EntradaVehiculo(models.Model):
    visitante = models.ForeignKey(F_Visitantes, on_delete=models.CASCADE, null=True, blank=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    guardia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placas = models.CharField(max_length=50)
    nota = models.CharField(max_length=50)

    def fechaformateada(self):
        return self.fecha.strftime("%m/%d %Y, %I:%M %p")

class Ausentismo(models.Model):
    TURNO = (
        ("día", "Día"),
        ("noche", "Noche")
    )

    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50)
    motivo = models.TextField(default="")
    turno = models.CharField(max_length=50, choices=TURNO, default="dia")
    
class ActividadesPreventivas(models.Model):
    TURNO = (
        ("día", "Día"),
        ("noche", "Noche")
    )
    
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    actividad = models.CharField(max_length=50, default="")
    cantidad = models.IntegerField()
    turno = models.CharField(max_length=50, choices=TURNO, default="dia")
    
class GuardTracking(models.Model):
    planta = models.ForeignKey(Planta,  on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_guardtracking")
    lat =  models.TextField()
    lng =  models.TextField()

#Modelos para Gestion de Capacitacion
class Categoria_Curso(models.Model):
    nombre = models.CharField('CategorÃ­a', max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Grado(models.Model):
    nombre = models.CharField('Grado', max_length=100)
    
    def __str__(self):
        return self.nombre
    
class Curso(models.Model):
    nombre = models.CharField('Curso', max_length=100)
    grado = models.ForeignKey(Grado,  on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria_Curso,  on_delete=models.CASCADE)  
    
    def __str__(self):
        return self.nombre  

class Concentracion(models.Model):    
    no_orden = models.CharField('No. Orden', max_length=50)    
    calificacion = models.SmallIntegerField('CalificaciÃ³n', blank=True, null=True)
    fecha_aplicacion = models.DateTimeField('Fecha de AplicaciÃ³n', blank=True, null=True, default = now)
    veces_aplicados = models.SmallIntegerField('Veces Aplicados', blank=True, null=True, default=1)
    tiempo_dedicado = models.SmallIntegerField('Tiempo Dedicado', blank=True, null=True, default=1)    
    user_aguilas = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_concentraciones", blank=True, null=True)
    puesto = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    sitio = models.ForeignKey(Planta, on_delete=models.SET_NULL, blank=True, null=True)    
    curso = models.ForeignKey(Curso,  on_delete=models.CASCADE, verbose_name="Curso", blank=True, null=True)   
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, blank=True, null=True)
    categoria = models.ForeignKey(Categoria_Curso, on_delete=models.CASCADE, blank=True, null=True)  
    
    def __str__(self):
        return self.curso + ' ' + self.user_aguilas__first_name + ' '  + self.user_aguilas__last_name

#Modelos para Gestion de Formatos 
def validate_length(value,length=10):
    if len(str(value))<length:
        raise ValidationError(u'%s debe ser mayor de 10 caracteres' % value)
    
class Paqueteria(models.Model): #Control de Entrada de Correspondencia
    fecha = models.DateTimeField('Entrada', default=now)
    guia = models.CharField('No. Guía', max_length=50, default="")
    empresa = models.CharField('Compañía', max_length=100)
    nombre = models.CharField('Remitente', max_length=100)
    destinatario = models.CharField('Destinatario', max_length=100)  
    bolfaltainfo = models.BooleanField('Falta de Información / Títulos mal puestos', default=False)  
    bolcables = models.BooleanField('Salen cables al paquete / bulto', default=False)  
    bolpolvo = models.BooleanField('Muestra evidencia de polvo', default=False)  
    bololor = models.BooleanField('Olor extraño en el paquete', default=False)  
    bolfuerahorario = models.BooleanField('Se entrega fuera de horario', default=False)      
    nota = models.TextField('Nota', default="", max_length=500, validators=[validate_length])
    user_aguilas = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_recibio")
    un = models.ForeignKey(Planta, on_delete=models.CASCADE, related_name="planta_paqueteria")
    
    class Meta:
        get_latest_by = ['-id']
        ordering = ['-id']
    
    def __str__(self):
        return "Destinatario: " + self.destinatario + " |  Guía: " + self.guia

class Empleado_Sin_Gafete(models.Model):
    empleado = models.CharField('Empleado', max_length=100)
    bolgafetepersonal = models.BooleanField('Gafete Personal', default=False)  
    bolgafetevehicular = models.BooleanField('Gafete Vehicular', default=False)  
    no_emp = models.CharField('No. de Empleado', max_length=12)
    departamento = models.CharField('Departamento', max_length=100)
    jefe = models.CharField('Supervisor', max_length=100)
    fecha = models.DateTimeField('Fecha Entrada', default=now)
    fecha_salida = models.DateTimeField('Fecha Salida', blank=True, null=True)
    turno = models.CharField('Turno', max_length=100)
    motivo = models.TextField('Motivo', blank=True, null=True, default="")   
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True, related_name="planta_empleadosingafete")
    user_aguilas = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.no_emp + " " + self.empleado
    
class Area_Restringida(models.Model):    
    TIEMPOS = (
        ("t0", "0"),
        ("t15", "15 minutos"),
        ("t30", "30 minutos"),
        ("t45", "45 minutos"),
        ("t60", "60 minutos"),
        ("t90", "90 minutos"),
        ("t120", "120 minutos")
    )
    
    no_emp = models.CharField('No. de Empleado / No. Gafete', max_length=12, blank=True, null=True)
    nombre = models.CharField('Nombre', max_length=100)
    departamento = models.CharField('Departamento / Empresa', max_length=100, blank=True, null=True)    
    fecha = models.DateTimeField('Fecha Entrada', default=now)
    fecha_salida = models.DateTimeField('Fecha Salida', blank=True, null=True)
    anfitrion = models.CharField('Nombre de quien autorizó', max_length=100)    
    tiempo = models.CharField('Tiempo', choices = TIEMPOS, max_length=50, default="t15")
    nota = models.TextField('Nota', default="")       
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True, related_name="planta_arearestringida")
    user_aguilas = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name="user_recibioarea")
    
    def __str__(self):
        return self.nombre
    
class EstadoFuerza(models.Model):
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, blank=True, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    fecha_inicio = models.DateField('Fecha de Inicio de Semana', blank=True, null=True)        
    no_orden = models.CharField('No. de Orden', max_length=12, blank=True, null=True)    
    ld = models.SmallIntegerField('Lunes Primero', default=0)    
    ln = models.SmallIntegerField('Lunes Segundo', default=0)    
    md = models.SmallIntegerField('Martes Primero', default=0)    
    mn = models.SmallIntegerField('Martes Segundo', default=0)  
    mid = models.SmallIntegerField('Miércoles Primero', default=0)    
    min = models.SmallIntegerField('Miércoles Segundo', default=0)  
    jd = models.SmallIntegerField('Jueves Primero', default=0)    
    jn = models.SmallIntegerField('Jueves Segundo', default=0)  
    vd = models.SmallIntegerField('Viernes Primero', default=0)    
    vn = models.SmallIntegerField('Viernes Segundo', default=0)  
    sd = models.SmallIntegerField('Sábado Primero', default=0)    
    sn = models.SmallIntegerField('Sábado Segundo', default=0)  
    dd = models.SmallIntegerField('Domingo Primero', default=0)    
    dn = models.SmallIntegerField('Domingo Segundo', default=0)  
    
    def __str__(self):
        return str(self.fecha_inicio) +" "+self.planta.nombre+" | "+self.role.alias_rol

    def fecha_l(self):
        return self.fecha_inicio

    def fecha_m(self):
        return self.fecha_inicio+timedelta(days=1)

    def fecha_mi(self):
        return self.fecha_inicio+timedelta(days=2)

    def fecha_j(self):
        return self.fecha_inicio+timedelta(days=3)

    def fecha_v(self):
        return self.fecha_inicio+timedelta(days=4)

    def fecha_s(self):
        return self.fecha_inicio+timedelta(days=5)

    def fecha_d(self):
        return self.fecha_inicio+timedelta(days=6)

    def total_l(self):
        return self.ld+self.ln

    def total_m(self):
        return self.md+self.mn

    def total_mi(self):
        return self.mid+self.min

    def total_j(self):
        return self.jd+self.jn

    def total_v(self):
        return self.vd+self.vn

    def total_s(self):
        return self.sd+self.sn

    def total_d(self):
        return self.dd+self.dn

    def totalDia(self):
        return (self.ld+self.md+self.mid+self.jd+self.vd+self.sd+self.dd)

    def totalNoche(self):
        return (self.ln+self.mn+self.min+self.jn+self.vn+self.sn+self.dn)

    def total(self):
        return (self.ld+self.md+self.mid+self.jd+self.vd+self.sd+self.dd+self.ln+self.mn+self.min+self.jn+self.vn+self.sn+self.dn)
    
    def horas(self):
        return self.total()*12
    
    def personas(self):
        return self.horas()/60

    def val(date_from, date_to):
        total = 0 

        return total

    def generate_json(self):
        jdias = []
        cobertura = self.cobertura_set.first()
        cubiertos_l = 0
        cubiertos_m = 0
        cubiertos_mi = 0
        cubiertos_j = 0
        cubiertos_v = 0
        cubiertos_s = 0
        cubiertos_d = 0
        if cobertura != None:
            cubiertos_l = cobertura.total_l()
            cubiertos_m = cobertura.total_m()
            cubiertos_mi = cobertura.total_mi()
            cubiertos_j = cobertura.total_j()
            cubiertos_v = cobertura.total_v()
            cubiertos_s = cobertura.total_s()
            cubiertos_d = cobertura.total_d()

        jdia_l = { 
            "fecha": str(self.fecha_l()),
            "turnos": self.total_l(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_l,
        }
        jdia_m = { 
            "fecha": str(self.fecha_m()),
            "turnos": self.total_mi(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_m,
        }
        jdia_mi = { 
            "fecha": str(self.fecha_mi()),
            "turnos": self.total_mi(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_mi,
        }
        jdia_j = { 
            "fecha": str(self.fecha_j()),
            "turnos": self.total_j(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_j,
        }
        jdia_v = { 
            "fecha": str(self.fecha_v()),
            "turnos": self.total_v(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_v,
        }
        jdia_s = { 
            "fecha": str(self.fecha_s()),
            "turnos": self.total_s(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_s,
        }
        jdia_d = { 
            "fecha": str(self.fecha_d()),
            "turnos": self.total_d(),
            "cobertura_exist": (cobertura != None),
            "cubiertos": cubiertos_d,
        }

        fjson = {
            str(self.fecha_l()): jdia_l,
            str(self.fecha_m()): jdia_m,
            str(self.fecha_mi()): jdia_mi,
            str(self.fecha_j()): jdia_j,
            str(self.fecha_v()): jdia_v,
            str(self.fecha_s()): jdia_s,
            str(self.fecha_d()): jdia_d,
        }

        return fjson



class Cobertura(models.Model):
        
    estadofuerza = models.ForeignKey(EstadoFuerza, on_delete=models.CASCADE, blank=True, null=True)
    ld = models.SmallIntegerField('Lunes Primero', default=0)    
    ln = models.SmallIntegerField('Lunes Segundo', default=0)    
    md = models.SmallIntegerField('Martes Primero', default=0)    
    mn = models.SmallIntegerField('Martes Segundo', default=0)  
    mid = models.SmallIntegerField('Miércoles Primero', default=0)    
    min = models.SmallIntegerField('Miércoles Segundo', default=0)  
    jd = models.SmallIntegerField('Jueves Primero', default=0)    
    jn = models.SmallIntegerField('Jueves Segundo', default=0)  
    vd = models.SmallIntegerField('Viernes Primero', default=0)    
    vn = models.SmallIntegerField('Viernes Segundo', default=0)  
    sd = models.SmallIntegerField('Sábado Primero', default=0)    
    sn = models.SmallIntegerField('Sábado Segundo', default=0)  
    dd = models.SmallIntegerField('Domingo Primero', default=0)    
    dn = models.SmallIntegerField('Domingo Segundo', default=0)  

    def total_l(self):
        return self.ld+self.ln

    def total_m(self):
        return self.md+self.mn

    def total_mi(self):
        return self.mid+self.min

    def total_j(self):
        return self.jd+self.jn

    def total_v(self):
        return self.vd+self.vn

    def total_s(self):
        return self.sd+self.sn

    def total_d(self):
        return self.dd+self.dn

    def totalDia(self):
        return (self.ld+self.md+self.mid+self.jd+self.vd+self.sd+self.dd)

    def totalNoche(self):
        return (self.ln+self.mn+self.min+self.jn+self.vn+self.sn+self.dn)

    def total(self):
        total = int(self.ld)+int(self.md)+int(self.mid)+int(self.jd)+int(self.vd)+int(self.sd)+int(self.dd)+int(self.ln)+int(self.mn)+int(self.min)+int(self.jn)+int(self.vn)+int(self.sn)+int(self.dn)
        #print("total cobertura "+str(total))
        return total
        #return 10
    def porcentaje(self):
        return (self.total()/self.estadofuerza.total())*100

class Falta(models.Model):

    TURNO = (
        ('día', 'Día'),
        ('noche', "Noche")
    )
    reportado_por = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField("Fecha", default=now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True)
    turno = models.CharField('Turno', choices=TURNO, max_length=100)
    motivo = models.TextField('Motivo', blank=True, null=True, default="") 

class Baja(models.Model):
    TURNO = (
        ('día', 'Día'),
        ('noche', "Noche")
    )
    #guardia = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="guardia_bajas")
    reportado_por = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    fecha = models.DateField("Fecha", default=now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True)
    turno = models.CharField('Turno', choices=TURNO, max_length=100)
    motivo = models.TextField('Motivo', blank=True, null=True, default="")
       
class Patio(models.Model):
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE,blank=True,null=True,related_name="planta_patio")

class Cajon(models.Model):
    trailer_id = models.IntegerField(null=True)
    disponibilidad = models.IntegerField(default=0, null=True)
    patio = models.ForeignKey(Patio, on_delete=models.CASCADE,blank=True,null=True)
    tipo_caja = models.CharField(max_length=20, blank=True, null=True)

class RecibosAlmacen(models.Model):
    no_emp = models.CharField('No. de Empleado / No. Gafete', max_length=12, blank=True, null=True)
    empleado = models.CharField('Empleado', max_length=100)
    fecha = models.DateTimeField('Fecha', default=now)
    departamento = models.CharField('Departamento / Empresa', max_length=100)    
    jefe = models.CharField('Jefe', max_length=100)        
    turno = models.CharField('turno', max_length=50, blank=True, null=True)    
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True, related_name="planta_recibos")
    user_aguilas = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name="user_recibos")
   
    proveedor = models.CharField('Nombre del Proveedor', max_length=100, blank=True, null=True)   
    empresa = models.CharField('Empresa', max_length=100, blank=True, null=True)   
    num_economico = models.CharField('Número Económico', max_length=100, blank=True, null=True) 
    num_caja = models.CharField('Número de Caja', max_length=100, blank=True, null=True)         
  
class RecibosItems(models.Model):
    TIPOUNIDAD = (
        ("kgs", "Kgs"),
        ("litros", "Litros"),
        ("metros", "Metros"),
        ("piezas", "Piezas"),
        ("cajas", "Cajas"),
        ("tarima", "Tarima")
    )
    
    recibo = models.ForeignKey(RecibosAlmacen, on_delete=models.CASCADE, related_name="recibo_items")
    cantidad = models.FloatField('Cantidad', default=0)
    unidad = models.CharField(choices=TIPOUNIDAD, max_length=20, default="kgs") 
    desc = models.TextField('Descripción', max_length=500, default="")
    noparte = models.CharField('No. de Parte', max_length=20)
    origen = models.CharField('Origen', max_length=100)
    destino = models.CharField('Destino', max_length=100)    
    fecha = models.DateTimeField('Fecha', default=now)
    fecha_salida = models.DateTimeField('Fecha', blank=True, null=True)
    
    def __str__(self):
        return "Cantidad: " + str(self.cantidad) + " " + " Unidad: " + self.unidad + " Desc: " + self.desc
        
class Logro(models.Model):
    
    ESTATUS = (
        ("Realizada", "Realizada"),
        ("Pendiente", "Pendiente")         
    )

    user_aguilas = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="user_logro", blank=True, null=True) 
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE, blank=True, null=True)
    fecha = models.DateTimeField('Fecha Logro', blank=True, null=True)
    logro = models.CharField('Nombre del Logro', max_length=100)
    accion = models.CharField('Motivo', max_length=254)    
    estatus = models.CharField('Estatus', choices=ESTATUS, max_length=50)
    observaciones = models.TextField('Observaciones', blank=True, null=True) 

    def __str__(self):
        return self.logro
