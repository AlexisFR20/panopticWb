from io import BytesIO
from core.models import Cliente, Planta
from arnes.models import Papeleta
from analytics.models import Rondin, RondinHecho, EvidenciaPunto, EstadoFuerza, F_18_puntos_Trailer
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from functools import reduce
from django.db.models import Q
from django.utils import timezone
import datetime as dt
import pytz

# Regresa una respuesta en formato de PDF dado un objecto HTML
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
    
# Detemina si el rol propocionado esta en la lista de los roles dados - True si cumple
def permiso(roles, role):
    acceso = False    
    if role in roles:
        acceso = True       
    return acceso

#Determine el cliente del usuario
def getCliente(user):
    return user.cliente

#Determine las plantas del cliente dado, como un querySet aún cuando se retorne sólo una
def getPlantas(cliente):
    plantaQuerySet = None    
    plantaQuerySet = Planta.objects.filter(cliente=cliente)
    return plantaQuerySet
  
# Regresa lista de clientes según los roles proporcionados
# Si no está dentro de los tales, regresa el cliente a donde pertenece
def getClientesLista(roles, user):
    clientes = None   
    role = user.role.alias_rol
    if role in roles:
        clientes = Cliente.objects.all()
    else:
        try:            
            clientes = Cliente.objects.filter(pk=user.cliente.id)
        except:
            clientes = None
    return clientes

def getRondines(planta_id):
    start = dt.date.today()
    start = start.replace(day = start.day + 1)
    if start.month == 1:
        lastmonth = start.replace(month = 12, year = start.year - 1)
    else:
        lastmonth = start.replace(month = start.month - 1)
    
    planta = planta_id
    rondines = Rondin.objects.filter(planta_id=planta)
    cantRondinesHechos = 0
    incidentes = 0
    rondineshechos = None

    if rondines:
        rondineshechos = RondinHecho.objects.filter(reduce(lambda x, y: x | y, [Q(rondin_id=item.id) for item in rondines])).filter(hora_inicio__range=[lastmonth,start])
        if rondineshechos is not None:
            cantRondinesHechos = rondineshechos.count()
            for p in rondineshechos:
                if EvidenciaPunto.objects.filter(rondinhecho_id = p.id).first() is not None:
                    incidentes += 1

    return cantRondinesHechos, incidentes

def getCobertura(planta_id):
    turnos = 0
    cubiertos = 0
    cobertura = 0.
    planta  = Planta.objects.get(pk=planta_id)
    if planta!=None:
        estadosfuerza = EstadoFuerza.objects.filter(planta=planta).order_by("-fecha_inicio")
        for ef in estadosfuerza:
            turnos = turnos + ef.total()
            if ef.cobertura_set.first():
                cubiertos = cubiertos + ef.cobertura_set.first().total()
        if turnos != 0:
            cobertura = round((cubiertos/turnos*100),2)
    else:
        cobertura = 0
    return cobertura

def get18puntos(planta):
    start = dt.date.today()
    start = start.replace(day = start.day + 1)
    if start.month == 1:
        lastmonth = start.replace(month = 12, year = start.year-1)
    else:
        lastmonth = start.replace(month = start.month - 1)

    #puntos18 = F_18_puntos_Trailer.objects.filter(planta_id=planta).filter(fecha__range=[lastmonth,start])
    puntos18 = F_18_puntos_Trailer.objects.filter(planta_id=planta)
    columnas = ["defensa","motor","llantas","piso_cabina","tanque_conbustible","cabina"
                ,"suspension_aire","flecha_embrague","quinta_rueda","debajo_plataforma"
                ,"puertas_internas_externas","piso_interior_cajas","paredes_laterales"
                ,"pared_frontal","techo","unidad_refrigeracion","escape","revision_sello"]
    incidencias = 0
    
    for punto in puntos18:
        for c in columnas:
            if getattr(punto, c) > 0: incidencias+=1
     
    return puntos18.count(),incidencias

def getVulnerabilidadGeneral(planta):
    papeletas = Papeleta.objects.filter(planta_id=planta).all().order_by('fecha').reverse()

    pencuestas = []
    pencuestas_ids = []
    p_ids = []
    
    #Get unique encuestas
    for penc in papeletas.order_by("encuesta_id","-fecha"): 
        if penc.encuesta_id not in pencuestas_ids:
            pencuestas.append(penc)
            p_ids.append(penc.id)
            pencuestas_ids.append(penc.encuesta_id)

    papeletas = Papeleta.objects.filter(id__in=p_ids)
    #agrupadas por categorias
    vinfraestructura = papeletas.filter(encuesta__categoria_id=1).all() #id 1 para infraestructura
    vsegop = papeletas.filter(encuesta__categoria_id=2).all() #id 2 para Seguridad operativa
    vsegelec = papeletas.filter(encuesta__categoria_id=3).all() #id 3 para seguridad electronica
    vlogistica = papeletas.filter(encuesta__categoria_id=4).all() #id 4 para logistica
    ventorno = papeletas.filter(encuesta__categoria_id=5).all() #id 5 para entorno

    #calculos de vulneravilidad promedio
    avgvinfra = 0
    avgvsegop = 0
    avgvsegelec = 0
    avgvlogi = 0
    avgvent = 0

    encuestas_ids = []
    encuestas_names = []

    for v in vinfraestructura:
        avgvinfra += v.calcularVulnerabilidad()/vinfraestructura.count()
        if v.encuesta.nombre not in encuestas_names:
            encuestas_names.append(v.encuesta.nombre)

    for v in vsegop:
        avgvsegop += v.calcularVulnerabilidad()/vsegop.count()
        if v.encuesta.nombre not in encuestas_names:
            encuestas_names.append(v.encuesta.nombre)

    for v in vsegelec:
        avgvsegelec += v.calcularVulnerabilidad()/vsegelec.count()
        if v.encuesta.nombre not in encuestas_names:
            encuestas_names.append(v.encuesta.nombre)

    for v in vlogistica:
        avgvlogi += v.calcularVulnerabilidad()/vlogistica.count()
        if v.encuesta.nombre not in encuestas_names:
            encuestas_names.append(v.encuesta.nombre)

    for v in ventorno:
        avgvent += v.calcularVulnerabilidad()/ventorno.count()
        if v.encuesta.nombre not in encuestas_names:
            encuestas_names.append(v.encuesta.nombre)

    vulnerabilidadGeneral = (avgvinfra+avgvsegop+avgvsegelec+avgvlogi+avgvent) / 5
    return vulnerabilidadGeneral
