from email.policy import default
from django.db import models
from core.models import Cliente, Planta, User
from django_resized import ResizedImageField
from django.utils.timezone import now
import jsonfield
 
class gpsdevice(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)
    deviceid = models.CharField(max_length=10, blank=True, null=True)
    devicename = models.CharField(max_length=20, blank=True, null=True)
    deviceesn = models.CharField(max_length=20, blank=True, null=True)
    asignado = models.BooleanField('Asignado', default=False)  
    activo = models.BooleanField('Activo', default=False)  
    tipo = models.BooleanField('tipo_dispositivo', default=False)
    
    def __str__(self):
        return self.devicename
    
class TipoVehiculo(models.Model):
    nombre = models.CharField("Nombre", max_length=50)
    descripcion = models.CharField("Descripcion corta", max_length=150)
      
    def __str__(self):
        return self.nombre 		

class Vehiculo(models.Model):
    placas = models.CharField("Placas", max_length=50)
    economico = models.CharField("No. Económico", max_length=50, blank=True, null=True)
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.SET_NULL, blank=True, null=True)
    marca = models.CharField("Marca",max_length=50)
    modelo = models.CharField("Modelo", max_length=50)
    anio = models.CharField("Año", max_length=10)
    seria = models.CharField("No. de Serie", max_length=50)
    gpsid = models.CharField(max_length=20, blank=True, null=True)
    gpsdevice = models.ForeignKey(gpsdevice, on_delete=models.SET_NULL, blank=True, null=True)
    disponible = models.BooleanField('¿Disponible?', default=True)  
    
    def natural_key(self):
        return self.marca+" "+self.modelo+" "+self.anio+" placas: "+self.placas
    
    def __str__(self):
        return self.marca+" "+self.modelo+" "+self.anio+" placas: "+self.placas
		
#tentativa a borrar
class Ruta(models.Model):
    valor = models.FloatField()
    unidad_valor = models.CharField(max_length=30, blank=True, default='')
    tiempo_estimado = models.FloatField() #en horas 
    nombre_chofer = models.CharField(max_length=50, blank=True, default='')
    matricula = models.CharField(max_length=30, blank=True, default='')
    destino = models.CharField(max_length=100, blank=True, default='')
    compania = models.CharField(max_length=50, blank=True, default='')
    
class gpstracking(models.Model):    
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, blank=True, null=True)    
    gpsid = models.CharField(max_length=20, blank=True, null=True)
    momento = models.DateTimeField('Fecha/Hora', blank=True, null=True)
    lat = models.FloatField("Latitud", blank=True, null=True)
    lng = models.FloatField("Longitud", blank=True, null=True)    
    
# Proveedor
class Proveedor(models.Model):
    nombre = models.CharField('Nombre Completo', max_length=50)
    empresa = models.CharField('Empresa Transportista', max_length=50)
    email = models.EmailField('Correo Electrónico', max_length=254)
    telefono = models.CharField('Teléfono', max_length=128, default='')
    domicilio = models.CharField(max_length = 100, default='') 
    razon_social = models.CharField(max_length = 100)    
    imagen_logo = models.ImageField('Imagen', upload_to='fotos_proveedores', blank=True, null=True) 

    def __str__(self):
        return self.empresa  

class Movimiento(models.Model):    
    
    CAT_ESTATUS = (
        ("Normal", "Normal"),
        ("Medio", "Medio"),
        ("Relevante", "Relevante"),   
        ("Finalizado", "Finalizado")        
    )
    
    TIPO_INC = (
        (1, "Normal"),
        (2, "Camino Bloqueado"),   # Medio
        (3, "Climatológico"),
        (4, "Demora en carga"),
        (5, "Demora en descarga"),
        (6, "Detención por Federales"),        
        (7, "Detención por Guardia Nacional"),
        (8, "Detención por Tránsito"),
        (9, "Descanso"),
        (10, "Falla Mecánica Leve-Moderada"),
        (11, "Incendio"),
        (12, "Incidencia en DOT"),
        (13, "Manifestación / Huelga"),
        (14, "Ponchadura de neumáticos"),
        (15, "Problema de Salud"),   # Medio
        (16, "Falla mecánica grave"),  # Relevante
        (17, "Carga equivocada"),
        (18, "Incidente Vial"),
        (19, "Contaminación de carga"),
        (20, "Decomiso de Mercancía"),
        (21, "Robo"),   # Relevante
        (22, "Otro")
    )
    
    nombre = models.CharField("Nombre / Alias del Movimiento",  max_length=100, blank=True, null=True)
    tipo_incidente = models.IntegerField("Tipo de Incidente", choices=TIPO_INC, blank=True, null=True, default=1)
    estatus = models.CharField("Estatus", choices=CAT_ESTATUS, max_length=30,  blank=True, null=True, default="Normal")    
    planta = models.ForeignKey(Planta, on_delete=models.SET_NULL, blank=True, null=True)
    chofer = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="chofer_movimiento")
    relevo = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="relevo_movimiento")
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, blank=True, null=True)  
    emp_transp = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, blank=True, null=True)  
    infocarga = models.TextField("Información de la Carga",  default="")
    tipo_movimiento = models.CharField("Tipo de movimiento",  max_length=50, blank=True, null=True)
    doc_completa = models.BooleanField('¿Documentación completa?', default=False)  
    origen = models.CharField("Direccion de origen", max_length=150, blank=True, null=True) 
    destino = models.CharField("Direccion destino", max_length=150, blank=True, null=True)
    origen_coords = models.CharField("Coordenadas de origen", max_length=50, blank=True, null=True)
    destino_coords = models.CharField("Coordenadas de destino", max_length=50,  blank=True, null=True)    
    waypoints=jsonfield.JSONField(null=True, blank=True)
    tiempo_estimado = models.CharField("Tiempo estimado", max_length=50,  blank=True, null=True)
    tiempo_estimado_google = models.CharField("Tiempo estimado google", max_length=50,  blank=True, null=True)
    fecha = models.DateTimeField('Tiempo de Salida', auto_now=True)
    fecha_fin = models.DateTimeField('Tiempo de Salida', blank=True, null=True)        
    confirmacion = models.BooleanField('Confirmación por Monitorista de Traslado Finalizado?', default=False)  
    remolque = models.CharField("Identificador del remolque",max_length=30, blank=True, null=True)   
    n_sello = models.CharField("Sello",max_length=100, blank=True, null=True) 
    valor_carga = models.CharField("Valor en carga", max_length=50, default='')
    peso = models.CharField("Peso de carga", max_length=50, default='')    
    gls = models.FloatField("Gls.", blank=True, null=True)
    lts = models.FloatField("Lts.", blank=True, null=True)
    puente = models.BooleanField(default=False)
    peaje = models.FloatField("Peaje.", blank=True, null=True) 
    ef = models.BooleanField(default=False) #Si llegó o finalizo el movimiento
    sobreruta = models.BooleanField(default=True) 

    def __str__(self):
        return "ID: "+str(self.id)+" "+self.origen+" - "+self.destino  

class IncidenteVial(models.Model):
   movimiento = models.ForeignKey(Movimiento, on_delete=models.SET_NULL, blank=True, null=True)
   ubigpslat = models.FloatField("Ubicación Lat") 
   ubigpslng = models.FloatField("Ubicación Lng") 
   fecha = models.DateTimeField('Tiempo del Incidente Vial', default=now)
   tipo = models.CharField('Tipo de Incidente', max_length=100)
   notas = models.TextField('Observaciones', max_length=700)
   estatus = models.CharField('Estatus', max_length=20)
   
   def __str__(self):
        return self.tipo + " | " + self.estatus   
        
class EvidenciaIncidenteVial(models.Model):
   incidente = models.ForeignKey(IncidenteVial, on_delete=models.SET_NULL, blank=True, null=True, related_name="evidencia_incidente_vial")
   evidencia = models.FileField(upload_to='evidencias/viales/%Y/%d/%m/')   
    
class Caja(models.Model):
    identificador = models.CharField("Identificador", max_length=50)
    capacidad = models.CharField("Capacidad", max_length=50)
    tipo = models.CharField("Tipo de caja", max_length=50)
    caja_no = models.CharField("No. de Caja", max_length=100, blank=True, null=True) 
    caja_placas = models.CharField("Placas de la caja", max_length=250, blank=True, null=True) 
    cajaeco = models.CharField("No. Económico de la caja", max_length=50, blank=True, null=True)
    sellocaja = models.CharField("Sello de Caja", max_length=50, blank=True, null=True)
    
class CajaMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, verbose_name="Movimiento", related_name="caja_movimiento") 
    caja = models.ForeignKey(Caja, on_delete=models.CASCADE, verbose_name="Caja", related_name="cajamov") 
    sello = models.CharField("Sello", max_length=30, default='')
    
    
class Tickets(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.SET_NULL, blank=True, null=True, related_name="movimiento_tickets")
    imagen = ResizedImageField('Foto', upload_to='fotos_tickets', blank=True, null=True, size=[1024, 1024], force_format='JPEG', quality=65)

class Carga(models.Model):

    TIPO = (
        ("Materia prima", "Materia prima"),
        ("Producto terminado", "Producto terminado"),
        ("Producto de ensamble", "Producto de ensamble"),
        ("Folio / Shipper", "Folio / Shipper"),
        ("Peso (en toneladas)", "Peso (en toneladas)"),
    )

    tipo = models.CharField("Tipo", choices=TIPO,  max_length=50)
    folio = models.CharField("Folio", max_length=50)
    peso = models.CharField("Peso", max_length=50)
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)


"""
class Punto(models.Model):
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
"""
    
