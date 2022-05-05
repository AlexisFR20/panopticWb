from django_resized import ResizedImageField
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, User
from django.db import models
from django_resized import ResizedImageField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator
from cporte.models import PorteCliente
import os

class Region(models.Model):
    nombre = models.CharField('Nombre de la región', max_length=128, default='Nombre de planta')    
    alias = models.CharField('Alias de Región', max_length=50, blank=True, default='')
    idnumerico = models.IntegerField('Identfiicador numérico', blank=True)    
    
    def __str__(self):
        return self.nombre
    
class Role(models.Model):
    nombre = models.CharField('Nombre del Rol / Cargo', max_length = 100)
    alias_rol = models.CharField('Alias: ', max_length = 100)
    grupo    = models.ForeignKey(Group, on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    nombre = models.CharField('Nombre', max_length=128, default='Nombre de sucursal')    
    domicilio = models.CharField('Domicilio', max_length=150, blank=True, default='')
    telefono = models.CharField('Teléfono', max_length=128, default='')
    ciudad = models.CharField('Ciudad', max_length=30, blank=True, default='')
    estado = models.CharField('Estado', max_length=30, blank=True, default='')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, blank=True, null=True, default=1)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    nombre = models.CharField(max_length = 100)
    razon_social = models.CharField(max_length = 100)
    domicilio = models.CharField(max_length = 100, default='') 
    corporativo = models.CharField('Corporativo', max_length=100, blank=True, null=True, default="")
    
    def getRazonSocial(self):
        return self.razon_social
    
    def getDomicilio(self):
        return self.domicilio
    
    def __str__(self):
        return self.nombre

"""
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
    path_privateKey = models.CharField(max_length=100, default = '')
    path_key = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['key'])])
    path_cer = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['cer'])])
    path_img = models.FileField(upload_to = upload_logo_to, validators=[FileExtensionValidator(allowed_extensions=['jpg','png'])], default='')

    def __str__(self):
        return self.nombre


class PorteReceiver(models.Model):
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
    path_privateKey = models.CharField(max_length=100, default = '')
    path_key = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['key'])])
    path_cer = models.FileField(upload_to = upload_photo_to, validators=[FileExtensionValidator(allowed_extensions=['cer'])])

    def __str__(self):
        return self.nombre


class PorteCarta(models.Model):
    json = models.JSONField()
    PorteReceiver = models.ForeignKey(PorteReceiver, on_delete=models.SET_NULL, blank=True, null=True)
    figura = models.CharField(max_length = 50)
    origen = models.CharField(max_length = 100)
    destino = models.CharField(max_length = 100)
    status = models.IntegerField(default=0)
"""

class Contacto(models.Model):
    nombre = models.CharField('Nombre del contacto', max_length=128)
    email = models.EmailField('E-mail', max_length=254)
    tel_pral = models.CharField('Teléfono Principal', max_length=128, default='')
    tel_alt = models.CharField('Teléfono Alterno', max_length=128, default='')
    posicion = models.CharField('Posición', max_length=128, default='')
    foto = ResizedImageField('Foto', upload_to='fotos_contactos', blank=True, null=True, size=[1024, 1024], force_format='JPEG', quality=65)    
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)    

    def __str__(self):
        return self.nombre
    
#Planta también conocida como Unidad de Negocio
class Planta(models.Model):

    STATUS = (
        ("optimo", "Óptimo"),
        ("estable", "Estable"),
        ("relevante", "Relevante")
    )
    
    nombre = models.CharField('Nombre', max_length=128)
    foto = ResizedImageField('Foto', upload_to='avatars', blank=True, null=True, size=[1024, 1024], force_format='JPEG', quality=65)    
    alias = models.CharField('Alias', max_length=50, blank=True, null=True)
    tipo = models.CharField('Tipo', max_length=50, blank=True, null=True)
    giro = models.CharField('Giro', max_length=50, blank=True, null=True)
    cinterno = models.ForeignKey(Contacto, blank=True, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField('Dirección', max_length=150, blank=True, null=True)
    ciudad = models.CharField('Ciudad', max_length=30, blank=True, null=True)
    estado = models.CharField('Estado', max_length=30, blank=True, null=True)
    pais = models.CharField('País', max_length=30, blank=True, null=True)
    lat = models.FloatField(blank=True, default=0, verbose_name="Latitud (coordenada)")
    lng = models.FloatField(blank=True, default=0, verbose_name="Longitud (coordenada)")      
    status = models.CharField(max_length=50, choices=STATUS, blank=True, null=True, default='optimo')
    slug = models.CharField('Slug', max_length=50, blank=True, null=True)    
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, blank=True, null=True)        
    gradio = models.IntegerField('Radio de Geocerca en Kms', default=2000)    
    polyradio = models.TextField('Puntos de Geo Cerca', blank=True, null=True)      
    sucursal = models.ForeignKey(Sucursal, on_delete=models.SET_NULL, blank=True, null=True)    
    estatus_cobertura_estable = models.IntegerField('Estatus Estable de Cobertura', default=0)
    estatus_cobertura_relevante = models.IntegerField('Estatus Relevante de Cobertura', default=0)
    estatus_ausentismo_estable = models.IntegerField('Estatus Estable de Ausentismo', default=0)
    estatus_ausentismo_relevante = models.IntegerField('Estatus Relevante de Ausentismo', default=0)
    estatus_rotacion_estable = models.IntegerField('Estatus Estable de Rotación', default=0)
    estatus_rotacion_relevante = models.IntegerField('Estatus Relevante de Rotación', default=0)   
    mails_zona = models.TextField('Emails para Notificacines en Zona 0 ',  blank=True, null=True)  
    mails_analisis_riesgo = models.TextField('Emails para Notificacines en Análisis de Riesgo ',  blank=True, null=True)  
    mails_dd = models.TextField('Emails para Notificacines en D&D Management ',  blank=True, null=True)  
    mails_predictive = models.TextField('Emails para Notificacines en Predictive Analytics ',  blank=True, null=True)      

    def natural_key(self):
        return (self.nombre)    

    def __str__(self):                                
        return self.nombre
    
    def getCinterno(self):
        selCinterno =  User.objects.get(pk=self.cinterno_id ) 
        return selCinterno           

class User(AbstractUser):    
    imagen = ResizedImageField('Foto', upload_to='avatars', blank=True, null=True, size=[1024, 1024], force_format='JPEG', quality=65)
    ceo = models.BooleanField(default=False)
    vicepresidente = models.BooleanField(default=False)
    vicepresidente_la = models.BooleanField(default=False)
    gerente_regional = models.BooleanField(default=False)
    gerente_planta = models.BooleanField(default=False)
    planta_plus = models.BooleanField(default=False)
    administrador = models.BooleanField(default=False)
    gerente_operativo = models.BooleanField(default=False)
    supervisor = models.BooleanField(default=False)
    supervidor_junior = models.BooleanField(default=False)
    ejecutivo_cuenta = models.BooleanField(default=False)
    monitorista = models.BooleanField(default=False)
    coordinador = models.BooleanField(default=False)
    jefe_grupo = models.BooleanField(default=False)
    guardia = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL, null = True)
    portecliente = models.ForeignKey(PorteCliente, on_delete = models.SET_NULL, null = True)
    planta = models.ForeignKey(Planta, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    tel_pral = models.CharField('Teléfono Principal', max_length=128, default='')
    tel_alt = models.CharField('Teléfono Alterno', max_length=128, default='')
    fecha_entrada = models.DateTimeField('Fecha de Entrada', blank=True, null=True)
    #Choferes
    no_orden = models.CharField('No. Orden', max_length=10, blank=True, null=True)
    edad = models.SmallIntegerField('Edad', blank=True, null=True)
    transportista = models.CharField('Empresa Transportista', max_length=100, blank=True, null=True)
    notification_token = models.CharField('Token de notificacion', max_length=250, blank=True, null=True)
    enservicio = models.BooleanField(default=False)
    
    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def getRol(self):
        rol = 'Sin asignar'
        if self.ceo == True: # Roles de cliente
            rol = 'CEO'
        elif self.vicepresidente == True:
            rol = 'VICEPRESIDENTE'
        elif self.vicepresidente_la == True:
            rol = 'VICEPRESIDENTE LA'
        elif self.gerente_regional == True:
            rol = 'GERENTE REGIONAL'
        elif self.gerente_planta == True:    
            rol = 'GERENTE DE PLANTA'
        elif self.planta_plus == True:
            rol = 'PLANTA PLUS'
        elif self.administrador == True: # A partir de aquí son los roles de Águilas
            rol = "ADMINISTRADOR"
        elif self.gerente_operativo == True:
            rol = "GERENTE OPERATIVO"
        elif self.supervisor == True:
            rol = "SUPERVISOR"
        elif self.supervidor_junior == True:
            rol = "SUPERVISOR JUNIOR"
        elif self.ejecutivo_cuenta == True:
            rol = "EJECUTIVO DE CUENTA"
        elif self.monitorista == True:
            rol = "MONITORISTA"
        elif self.coordinador == True:
            rol = "COORDINADOR"
        elif self.jefe_grupo == True:
            rol = "JEFE DE GRUPO"
        elif self.guardia == True:
            rol = "GUARDIA"
            
        return rol;
    
    def getRolAlias(self):
        alias = 'none'
        if self.ceo == True: # aliases de cliente
            alias = 'ceo'
        elif self.vicepresidente == True:
            alias = 'vicepresidente'
        elif self.vicepresidente_la == True:
            alias = 'vicepresidente_la LA'
        elif self.gerente_regional == True:
            alias = 'gerente_regional'
        elif self.gerente_planta == True:    
            alias = 'gerente_planta'
        elif self.planta_plus == True:
            alias = 'planta_plus'
        elif self.administrador == True: # A partir de aquí son los aliases de Águilas
            alias = "administrador"
        elif self.gerente_operativo == True:
            alias = "gerente_operativo"
        elif self.supervisor == True:
            alias = "supervisor"
        elif self.supervidor_junior == True:
            alias = "supervidor_junior"
        elif self.ejecutivo_cuenta == True:
            alias = "ejecutivo_cuenta"
        elif self.monitorista == True:
            alias = "monitorista"
        elif self.coordinador == True:
            alias = "coordinador"
        elif self.jefe_grupo == True:
            alias = "jefe_grupo"
        elif self.guardia == True:
            alias = "guardia"
            
        return alias;
    
    def getRol(self):        
        cargo = self.role
        return cargo
    
    def getRolU(self):        
        cargo = self.role.alias_rol
        return cargo
    
    def getClient(self):
        return self.cliente    
    
    def getPlanta(self):
        return self.planta
    
    def getGroup(self):
        return self.groups.all()[0].name == "groupname"

    def getLastTracking(self):
        track = self.user_guardtracking.order_by('-id').first()
        print("track "+str(track.id))
        return track
    
    class Meta:
        db_table = 'auth_user'
        
class Puesto(models.Model):
    nombre      = models.CharField('Nombre del Puesto', max_length=128, default='')    
    
    def __str__(self):
        return self.nombre
    
class Ciudad(models.Model):
    nombre = models.CharField('Ciudad', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Areapermiso(models.Model):
    nombre = models.CharField('Área del Permiso', max_length=50)
    alias = models.CharField('Alias', max_length=50)
    orden = models.SmallIntegerField('Orden', default=0)
    
def __str__(self):
        return self.nombre 
    
class Permisos(models.Model):
    nombre = models.CharField('Nombre del Permiso', max_length=50)
    desc = models.CharField('Descripción', max_length=50)
    estado = models.BooleanField('Estado', default=False)     
    areapermiso = models.ForeignKey(Areapermiso, on_delete=models.SET_NULL, blank=True, null=True)    
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)         

    def __str__(self):
        return self.nombre 
        
class Permrol(models.Model):
    permiso = models.ForeignKey(Permisos, on_delete=models.SET_NULL, blank=True, null=True)    
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)  
    estado = models.BooleanField('Estado', default=False)     
    activo = models.BooleanField('Activo', default=False)     

class Notificacion(models.Model):
    titulo  = models.CharField('Título',max_length=256)
    mensaje = models.TextField('Mensaje', blank=True, null=True)
    visto = models.BooleanField('¿Visto?',default=False)
    fecha = models.DateTimeField('Hora de Alarma', auto_now=True)
    modelo = models.CharField('Modelo Relacionado', max_length=256, blank=True, null=True)
    idproblema= models.IntegerField('Id_problema', blank=True, null=True)
    param_text  = models.CharField('Parámetros',max_length=256, blank=True, null=True)
    param_bol = models.BooleanField('Parámetro S/N', default=False)     
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)            

@receiver(post_save, sender=User)
def create_welcome_message(sender, **kwargs):
    if kwargs.get('created', False):
        Notificacion.objects.create(usuario=kwargs.get('instance'),titulo="Nuevo usuario registrado", mensaje="Bienvenido")

class  Clima(models.Model):
    ciudad  = models.CharField('Ciudad',max_length=120)
    codigo = models.TextField('Codigo', blank=True, null=True)
