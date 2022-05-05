from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from API.serializers import RondinSerializer
from entorno.models import Incidente, TipoIncidente
from analytics.models import *
from analytics.forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role, Sucursal, Notificacion
from core import user_validation
from core.views.views import ceo_global
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.sites.models import Site  
from arnes.models import Encuesta, Categoria_Encuesta, Pregunta, Papeleta, Respuesta, Recomendacion
from arnes.forms import EncuestaForm, PreguntaForm, PapeletaForm, RecomendacionForm
from ddmanagement.models import *
from ddmanagement.forms import *
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView, RequestConfig, tables
from django.urls import reverse, reverse_lazy
from administrador.tables import EncuestaTable, PreguntaTable, PapeletaTable, RespuestaTable, CategoriaTable
from administrador.processors import *
from datetime import datetime, date, time, timedelta
from django.db.models import Avg, Max, Min, Sum
from core import notifications
from core.externalModels import CiaaR1
from django.views.generic import View
from core.utils import *
import base64, secrets, io, os, shutil
from PIL import Image
from io import BytesIO
from django.contrib.sites.models import Site
import datetime as dt
from datetime import date
from pytz import timezone
import json

n = Notificacion.objects.filter(visto = False)

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']
# Obtenciión de lista mínima de usuarios de tipo cliente y de Águilas
ultimos_usuarios_aguilas  = User.objects.filter(groups__name='aguilas', is_active=1)[:5]
#ultimos_usuarios_clientes = User.objects.filter(groups__name='cliente', is_active=1)[:5]
ultimos_usuarios_clientes = Cliente.objects.all()[:5]


def admin_home(request):     
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') )      
    
    print("EL ROL DEL QUE ACCEDIO: ", request.user.role.alias_rol) 
    if(permisoBackstage(request).get("permisoBackstage")):
        return render(request, 'administrador/admin_home.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'ultimos_usuarios_aguilas': ultimos_usuarios_aguilas,  'ultimos_usuarios_clientes': ultimos_usuarios_clientes })
    else:
        return redirect("http://192.168.1.118:8001/")
    
def admin_dd_cerca_delictiva(request):
    userdict = user_validation.validate(request)
    planta = Planta.objects.get(pk= 4 )       
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_geocerca', 'js_wickedpicker', 'js_fancybox']           
  
    return render(request, 'administrador/ddmanagement/geocercas/cerca_delictiva_edit.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'planta': planta })

# Rangos de Fecha
def admin_rangos_fecha(request):
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id') )
    all_users   = User.objects.all()
    #l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    #l_as_list = list(l)      
    return render(request, 'rangos-de-fecha.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'all_users': all_users })

# Estados de Fuerza
def admin_estados_fuerza(request):    
    #revisiones = F_18_puntos_Trailer.objects.all()   
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    usuarios = User.objects.all()
    estadosfuerza = EstadoFuerza.objects.all().order_by("-fecha_inicio")
    print("fuerzas "+str(estadosfuerza.count()))

    return render(request, 'administrador/predictive/estados-fuerza.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "estadosfuerza": estadosfuerza})

def ajax_load_estados_fuerza(request):
    planta = Planta.objects.get(id=request.GET.get("planta_id"))

    inicio = datetime.strptime(request.GET.get("start"), '%Y-%m-%d')
    fin = datetime.strptime(request.GET.get("end"), '%Y-%m-%d')
    w_inicio = inicio;
    while w_inicio.weekday() != 0: #0 for monday
        w_inicio -= timedelta(days=1)
    print("semana_inicio "+str(w_inicio))
    
    estadosfuerza = EstadoFuerza.objects.filter(cliente_id=request.GET.get("cliente_id")).filter(planta_id=request.GET.get("planta_id")).filter(fecha_inicio__range=[w_inicio, fin]).all().order_by("-fecha_inicio")
    
    faltas = Falta.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha")
    print("faltas "+str(faltas.count()))
    bajas = Baja.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha")
    print("bajas "+str(bajas.count()))
    vacantes = Vacante.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha").aggregate(Sum('n_vacantes'))
    print(vacantes)


    turnos = 0
    cubiertos = 0
    cobertura = 0
    print(estadosfuerza)
    for ef in estadosfuerza:
            
        json = ef.generate_json()
        
        if ef.fecha_inicio < inicio.date():
            #code cortar semana

            date_from = inicio
            date_to = w_inicio+timedelta(days=6) #llega hasta el domingo 
            if date_to > fin:
                date_to = fin
            print("from "+str(inicio.date()))
            while date_from <= date_to:

                turnos += json.get(str(date_from.date())).get("turnos")
                cubiertos += json.get(str(date_from.date())).get("cubiertos")
                date_from += timedelta(days=1)
        elif fin < datetime.strptime(str(ef.fecha_inicio), '%Y-%m-%d')+timedelta(days=6):
            date_from = datetime.strptime(str(ef.fecha_inicio), '%Y-%m-%d')
            date_to = fin #llega hasta el domingo 
            if date_from < inicio:
                date_from = inicio
            while date_from <= date_to:

                turnos += json.get(str(date_from.date())).get("turnos")
                cubiertos += json.get(str(date_from.date())).get("cubiertos")
                date_from += timedelta(days=1)

        else:
            turnos += ef.total()
            print(turnos)
            if ef.cobertura_set.first() != None:
                cubiertos += ef.cobertura_set.first().total()


    if turnos > 0:
        cobertura = round(cubiertos/turnos*100, 2)


    return render(request, 'administrador/predictive/estados-fuerza_ajax.html', {"estadosfuerza": estadosfuerza, "planta": planta, 'faltas': faltas, 'bajas': bajas, 'vacantes': vacantes, 'inicio': inicio, 'fin': fin, "turnos": turnos, 'cubiertos': cubiertos, 'cobertura': cobertura})

def load_estados_fuerza_by_range(request):
    inicio = datetime.strptime(request.GET.get("start"), '%Y-%m-%d')
    print("inicio "+str(inicio))
    fin = datetime.strptime(request.GET.get("end"), '%Y-%m-%d')
    print("fin "+str(fin))
    w_inicio = inicio;
    while w_inicio.weekday() != 0: #0 for monday
        w_inicio -= timedelta(days=1)
    print("semana_inicio "+str(w_inicio))

    estadosfuerza = EstadoFuerza.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha_inicio__range=[w_inicio, fin]).all().order_by("-fecha_inicio")

    turnos = 0
    cubiertos = 0
    cobertura = 0
    bajas = 0
    rotacion= 0
    horas = 0
    personas = 0
    faltas = 0
    print(estadosfuerza)

    baja = Baja.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[inicio, fin]).count()
    bajas += baja
    falta = Falta.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[inicio, fin]).count()
    faltas += falta 
    

    for ef in estadosfuerza:
            
        json = ef.generate_json()
        
        if ef.fecha_inicio < inicio.date():
            #code cortar semana

            date_from = inicio
            date_to = w_inicio+timedelta(days=6) #llega hasta el domingo 
            if date_to > fin:
                date_to = fin
            print("from "+str(inicio.date()))
            while date_from <= date_to:
                turnos += json.get(str(date_from.date())).get("turnos")
                cubiertos += json.get(str(date_from.date())).get("cubiertos")
                date_from += timedelta(days=1)
        elif fin < datetime.strptime(str(ef.fecha_inicio), '%Y-%m-%d')+timedelta(days=6):
            date_from = datetime.strptime(str(ef.fecha_inicio), '%Y-%m-%d')
            date_to = fin #llega hasta el domingo 
            if date_from < inicio:
                date_from = inicio
            while date_from <= date_to:

                turnos += json.get(str(date_from.date())).get("turnos")
                cubiertos += json.get(str(date_from.date())).get("cubiertos")
                date_from += timedelta(days=1)

        else:
            turnos += ef.total()
            print(turnos)
            if ef.cobertura_set.first() != None:
                cubiertos += ef.cobertura_set.first().total()


    horas = turnos*12
    personas = horas/60
    ausentismo = 0

    if turnos > 0:
        cobertura = round(cubiertos/turnos*100, 2)
    if personas > 0:
        rotacion = round((bajas/personas)*100, 2)
    if turnos > 0:
        ausentismo = round(faltas/turnos*100, 2)

    rj = {
        "turnos": turnos,
        "cubiertos": cubiertos,
        "cobertura": cobertura,
        "horas": horas,
        "personas": personas,
        "rotacion": rotacion,
        "ausentismo": ausentismo
    }

    return JsonResponse(rj)

  
  
def admin_estados_fuerza_create(request):        
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()     
    usuarios = User.objects.all()
    sucursales = Sucursal.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':

        fuerza = EstadoFuerza()
        fuerza.cliente_id = request.POST.get("cliente_id")
        fuerza.planta_id = request.POST.get("planta_id")
        fuerza.sucursal_id = request.POST.get("sucursal_id")
        fuerza.role_id = request.POST.get("role_id")
        fuerza.fecha_inicio = request.POST.get("fecha_inicio")
        #fuerza.no_orden = request.POST.get("no_orden")
        fuerza.ld = request.POST.get("ld")
        fuerza.ln = request.POST.get("ln")
        fuerza.md = request.POST.get("md")
        fuerza.mn = request.POST.get("mn")
        fuerza.mid = request.POST.get("mid")
        fuerza.min = request.POST.get("min")
        fuerza.jd = request.POST.get("jd")
        fuerza.jn = request.POST.get("jn")
        fuerza.vd = request.POST.get("vd")
        fuerza.vn = request.POST.get("vn")
        fuerza.sd = request.POST.get("sd")
        fuerza.sn = request.POST.get("sn")
        fuerza.dd = request.POST.get("dd")
        fuerza.dn = request.POST.get("dn")

        fuerza.save();

        return redirect('administrador:admin_estados_fuerza')
    
    return render(request, 'administrador/predictive/estados-fuerza_create.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "roles": roles, 'sucursales': sucursales })

def admin_estados_fuerza_edit(request, id):

    fuerza = EstadoFuerza.objects.get(pk=id)

    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()     
    usuarios = User.objects.all()
    sucursales = Sucursal.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':

        fuerza.cliente_id = request.POST.get("cliente_id")
        fuerza.planta_id = request.POST.get("planta_id")
        fuerza.sucursal_id = request.POST.get("sucursal_id")
        fuerza.role_id = request.POST.get("role_id")
        fuerza.fecha_inicio = request.POST.get("fecha_inicio")
        #fuerza.no_orden = request.POST.get("no_orden")
        fuerza.ld = request.POST.get("ld")
        fuerza.ln = request.POST.get("ln")
        fuerza.md = request.POST.get("md")
        fuerza.mn = request.POST.get("mn")
        fuerza.mid = request.POST.get("mid")
        fuerza.min = request.POST.get("min")
        fuerza.jd = request.POST.get("jd")
        fuerza.jn = request.POST.get("jn")
        fuerza.vd = request.POST.get("vd")
        fuerza.vn = request.POST.get("vn")
        fuerza.sd = request.POST.get("sd")
        fuerza.sn = request.POST.get("sn")
        fuerza.dd = request.POST.get("dd")
        fuerza.dn = request.POST.get("dn")

        fuerza.save();

        return redirect('administrador:admin_estados_fuerza')
    
    return render(request, 'administrador/predictive/estados-fuerza_edit.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "roles": roles, 'sucursales': sucursales, 'fuerza': fuerza })

class EstadoFuerzaDelete(DeleteView):
    model = EstadoFuerza
    success_url = reverse_lazy('administrador:admin_estados_fuerza')
    template_name = 'administrador/predictive/estados_fuerza_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context



def admin_estados_fuerza_cobertura_create(request, id):    

    estadofuerza = EstadoFuerza.objects.get(pk=id)
    cobertura = estadofuerza.cobertura_set.first()

    if request.method == 'POST':

        if cobertura:
            cover = cobertura
        else:
            cover = Cobertura()
        cover.estadofuerza_id = id
        cover.ld = request.POST.get("ld")
        cover.ln = request.POST.get("ln")
        cover.md = request.POST.get("md")
        cover.mn = request.POST.get("mn")
        cover.mid = request.POST.get("mid")
        cover.min = request.POST.get("min")
        cover.jd = request.POST.get("jd")
        cover.jn = request.POST.get("jn")
        cover.vd = request.POST.get("vd")
        cover.vn = request.POST.get("vn")
        cover.sd = request.POST.get("sd")
        cover.sn = request.POST.get("sn")
        cover.dd = request.POST.get("dd")
        cover.dn = request.POST.get("dn")

        cover.save()

        noti = Notificacion()
        noti.titulo = "Cobertura creada en estado de fuerza"
        c = float(cover.total())
        print(c)
        e = float(estadofuerza.total())
        print(e)
        val = (c/e*100)
        print(val)
        noti.mensaje = "Se dio de alta una cobertura a "+str(round(val, 2))+"%"
        noti.modelo = "EstadoFuerza"
        noti.idproblema = estadofuerza.id
        noti.usuario_id = request.user.id
        noti.save()

        try:
            print("mandar notificacion de cobertura")
            notifications.sendNotification("Cobertura creada en estado de fuerza", "Se dio de alta una cobertura a "+str(round(val, 2))+"% del total de la semana", request.user.notification_token, request.user.email, noti)
        except:
            print("No se pudo enviar notificacion")

        try:
            print("mandar notificacion por planta")
            notifications.sendemailsbyplanta("Cobertura creada en estado de fuerza", "Se dio de alta una cobertura a "+str(round(val, 2))+"% del total de la semana", estadofuerza.planta, "predictive", noti)
        except Exception as error2:
            print("No se pudo enviar notificacion: "+str(error2))

        return redirect('administrador:admin_estados_fuerza')

    return render(request, 'administrador/predictive/estado_fuerza_cobertura_create.html', {'css_list': css_list, 'js_list': js_list, 'estadofuerza': estadofuerza, 'cobertura': cobertura})

class admin_falta_create(CreateView):
    model = Falta
    form_class = FaltaForm
    template_name = 'administrador/predictive/falta_form.html'

    def get_success_url(self):
        return reverse('administrador:admin_falta_list')

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.reportado_por = self.request.user
        #form.nombre = form.guardia.first_name+" "+form.guardia.last_name

        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs): 
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context


def admin_falta_list(request):
    faltas = Falta.objects.all()

    return render(request, 'administrador/predictive/faltas.html', { 'css_list': css_list, 'js_list': js_list, 'faltas': faltas })



def admin_falta_edit(request, id):
    falta = Falta.objects.get(pk=id)
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        falta.planta_id = request.POST.get('planta_id')
        falta.cliente_id = request.POST.get('cliente_id')
        falta.sucursal_id = request.POST.get('sucursal_id')
        falta.turno = request.POST.get('turno')
        falta.motivo = request.POST.get('motivo')
        falta.fecha = request.POST.get('fecha')
        falta.nombre = request.POST.get('nombre')

        falta.save()
        return redirect('administrador:admin_falta_list')


    return render(request, 'administrador/predictive/falta_edit.html', { 'css_list': css_list, 'js_list': js_list, 'falta': falta, 'plantas': plantas, 'clientes': clientes })

class FaltaDelete(DeleteView):
    model = Falta
    success_url = reverse_lazy('administrador:admin_falta_list')
    template_name = 'administrador/predictive/falta_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def admin_bajas_list(request):
    bajas = Baja.objects.all()

    return render(request, 'administrador/predictive/bajas.html', { 'css_list': css_list, 'js_list': js_list, 'bajas': bajas })

def admin_baja_edit(request, id):
    baja = Baja.objects.get(pk=id)
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()

    if request.method == 'POST':
        baja.nombre = request.POST.get('nombre')
        baja.planta_id = request.POST.get('planta_id')
        baja.cliente_id = request.POST.get('cliente_id')
        baja.sucursal_id = request.POST.get('sucursal_id')
        baja.turno = request.POST.get('turno')
        baja.motivo = request.POST.get('motivo')
        baja.fecha = request.POST.get('fecha')

        baja.save()
        return redirect('administrador:admin_baja_list')


    return render(request, 'administrador/predictive/baja_edit.html', { 'css_list': css_list, 'js_list': js_list, 'baja': baja, 'plantas': plantas, 'clientes': clientes })

def admin_baja_create(request):
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    guardias = User.objects.filter(role__alias_rol="guardia")
    turnos = Baja.TURNO

    if request.method == 'POST':
        baja = Baja()
        baja.reportado_por = request.user
        baja.nombre = request.POST.get('nombre')
        baja.planta_id = request.POST.get('planta_id')
        baja.cliente_id = request.POST.get('cliente_id')
        baja.sucursal_id = request.POST.get('sucursal_id')
        baja.turno = request.POST.get('turno')
        baja.motivo = request.POST.get('motivo')
        baja.fecha = request.POST.get('fecha')

        baja.save()
        return redirect('administrador:admin_baja_list')


    return render(request, 'administrador/predictive/baja_create.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'guardias': guardias, 'turnos': turnos })

class BajaDelete(DeleteView):
    model = Baja
    success_url = reverse_lazy('administrador:admin_baja_list')
    template_name = 'administrador/predictive/baja_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def admin_vacantes_list(request):
    vacantes = Vacante.objects.all()

    return render(request, 'administrador/predictive/vacantes.html', { 'css_list': css_list, 'js_list': js_list, 'vacantes': vacantes })

def admin_vacante_create(request):
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        vacante = Vacante()
        #baja.reportado_por = request.user
        vacante.planta_id = request.POST.get('planta_id')
        vacante.n_vacantes = request.POST.get('n_vacantes')
        vacante.observaciones = request.POST.get('observaciones')
        vacante.fecha = request.POST.get('fecha')
        vacante.role_id = request.POST.get('role_id')

        vacante.save()
        return redirect('administrador:admin_vacante_list')


    return render(request, 'administrador/predictive/vacante_create.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'roles': roles })

def admin_vacante_edit(request, id):
    vacante = Vacante.objects.get(pk=id)
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        #baja.reportado_por = request.user
        vacante.planta_id = request.POST.get('planta_id')
        vacante.n_vacantes = request.POST.get('n_vacantes')
        vacante.observaciones = request.POST.get('observaciones')
        vacante.fecha = request.POST.get('fecha')
        vacante.role_id = request.POST.get('role_id')

        vacante.save()
        return redirect('administrador:admin_vacante_list')


    return render(request, 'administrador/predictive/vacante_edit.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'roles': roles, 'vacante': vacante })

class VacanteDelete(DeleteView):
    model = Vacante
    success_url = reverse_lazy('administrador:admin_vacante_list')
    template_name = 'administrador/predictive/vacante_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context


def admin_entrada_equipo(request): 
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id'))    
    entradaequipos = EntradaEquipo.objects.all()    
    
    return render(request, 'administrador/predictive/entradaequipo.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'entradaequipos': entradaequipos })

def admin_visitantes(request):
    visitantes  = F_Visitantes.objects.all()
    
    return render(request, 'administrador/predictive/visitantes_lista.html', { 'css_list': css_list, 'js_list': js_list, 'visitantes': visitantes })

def admin_visitantes_registrar(request):
    visitantes  = F_Visitantes.objects.all()
    
    return render(request, 'administrador/predictive/visitantes_registrar.html', { 'css_list': css_list, 'js_list': js_list, 'visitantes': visitantes })

def admin_visitante_detalles(request, id):
    visitante  = F_Visitantes.objects.get(pk=id)
    
    return render(request, 'administrador/predictive/visitantes_detalle.html', { 'css_list': css_list, 'js_list': js_list, 'visitante': visitante })

def admin_incidentes_servicio(request):
    incidentes  = Incidentes.objects.all()
    
    return render(request, 'administrador/predictive/incidentesservicio.html', { 'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes })
    
def admin_incidentes_servicio_detalle(request, id):
    incidente  = Incidentes.objects.get(pk=id)
    if request.method == 'POST':
        incidente.acciones_tomadas = request.POST.get('acciones_tomadas');
        incidente.status = request.POST.get('status');
        incidente.save()
    
    return render(request, 'administrador/predictive/incidentesserviciodetalle.html', {'css_list': css_list, 'js_list': js_list, 'incidente': incidente})

def admin_empleados_sin_gafete(request):
    visitantes  = F_Visitantes.objects.all()
    
    return render(request, 'administrador/predictive/empleados_sin_gafete_lista.html', { 'css_list': css_list, 'js_list': js_list, 'visitantes': visitantes })

def admin_empleados_sin_gafete_registrar(request):
    visitantes  = F_Visitantes.objects.all()
    
    return render(request, 'administrador/predictive/empleados_sin_gafete_registrar.html', { 'css_list': css_list, 'js_list': js_list, 'visitantes': visitantes })

def admin_predictive_analytics_dashboard(request):  
    #Verifica que esté definido vcliene 
    cliente = request.user.cliente    
    if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
        plantas = Planta.objects.filter(cliente=cliente).all()
    elif request.user.role.alias_rol=='administrador':
        plantas = Planta.objects.all()
    elif request.user.role.alias_rol=='ceo':
        plantas = Planta.objects.filter(cliente=cliente).all()
    else:
        idplanta = request.user.planta.id
        plantas = Planta.objects.filter(id=idplanta).all()

    #return render(request, 'administrador/predictive/admin_predictive_analytics.html', { 'css_list': css_list, 'js_list': js_list 
    return render(request, 'administrador/predictive/dashboard/dashboard.html', { 'css_list': css_list, 'js_list': js_list, 'notificaciones': n, 'vcliente': cliente, 'vplantas': plantas })

class CategoriaEncuestaCreate(CreateView):
    model = Categoria_Encuesta
    fields = ["nombre"]
    template_name = 'administrador/arnes/categoria_encuesta_form.html'
    
    def get_success_url(self):
        return reverse('administrador:admin_list_encuestas')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class EncuestaCreate(CreateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'administrador/arnes/encuesta_form.html'
    
    def get_success_url(self):
        return reverse('administrador:admin_detail_encuesta', args=[self.object.id])
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class EncuestaDetail(DetailView):
    model = Encuesta
    template_name = 'administrador/arnes/encuesta_detail.html'

    def get_context_data(self, **kwargs):
        preguntas = Pregunta.objects.filter(encuesta_id=self.object.id)
        papeletas = Papeleta.objects.filter(encuesta_id=self.object.id)
        table = PreguntaTable(preguntas)
        tpapeletas = PapeletaTable(papeletas)
        RequestConfig(self.request, paginate=False).configure(table)
        RequestConfig(self.request, paginate=False).configure(tpapeletas)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        context['table'] = table
        context['tpapeletas'] = tpapeletas
        return context

class EncuestaUpdate(UpdateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'administrador/arnes/encuesta_update_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_update_encuesta', args=[self.object.id]) + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class EncuestaDelete(DeleteView):
    model = Encuesta
    success_url = reverse_lazy('administrador:admin_list_encuestas')
    template_name = 'administrador/arnes/encuesta_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class PreguntaCretae(CreateView):
    model = Pregunta
    form_class = PreguntaForm
    template_name = 'administrador/arnes/pregunta_form.html'
    
    def get_success_url(self, **kwargs):
        return reverse('administrador:admin_detail_encuesta', kwargs={'pk': self.kwargs.get("pk")} )

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))

        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        context['pk'] = self.kwargs.get("pk")

        return context

class PreguntaDelete(DeleteView):
    model = Pregunta
    template_name = 'administrador/arnes/pregunta_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_detail_encuesta', kwargs={'pk': self.object.encuesta_id})

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def admin_edit_papeleta(request, pk, id):

    pregunta = Pregunta.objects.get(id=id)

    if request.method == 'POST':
        pregunta.pregunta = request.POST.get('pregunta')
        pregunta.valor = request.POST.get('valor')
        pregunta.orden = request.POST.get('orden')
        pregunta.save()

        return redirect('administrador:admin_detail_encuesta', pk=pregunta.encuesta_id)

    return render(request, 'administrador/arnes/pregunta_edit.html', { 'css_list': css_list, 'js_list': js_list, 'pregunta': pregunta, 'pk': pk, 'id': id })


class encuestas(SingleTableView):
    
    table_class = EncuestaTable
    template_name = 'administrador/arnes/list_encuestas.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Encuesta.objects.filter(nombre__contains=query)
        else:
            lista = Encuesta.objects.all()
        return lista

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

"""
class AnalisisEncuestaCreate(CreateView):
    model = Analisis
    fields = ["nombre"]
    template_name = 'administrador/arnes/analisis_encuesta_form.html'
    
    def get_success_url(self):
        return reverse('administrador:admin_list_analisis')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class AnalisisUpdate(UpdateView):
    model = Analisis
    fields = ["nombre"]
    template_name = 'administrador/arnes/analisis_update_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_update_analisis', args=[self.object.id]) + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class AnalisisEncuesta(SingleTableView):
    table_class = AnalisisTable
    template_name = "administrador/arnes/list_analisis.html"
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Analisis.objects.filter(nombre__contains=query)
        else:
            lista = Analisis.objects.all()
        return lista

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context
"""

class CategoriasEncuesta(SingleTableView):
    table_class = CategoriaTable
    template_name = 'administrador/arnes/list_categorias.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Categoria_Encuesta.objects.filter(nombre__contains=query)
        else:
            lista = Categoria_Encuesta.objects.all()
        return lista

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class CategoriaUpdate(UpdateView):
    model = Categoria_Encuesta
    fields = ["nombre"]
    template_name = 'administrador/arnes/categoria_update_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_update_categoria', args=[self.object.id]) + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context
        
class MovimientoCreate(CreateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'administrador/ddmanagement/movimiento_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_movimientos_lista')
        
    def form_valid(self, form, **kwargs):        
        form = form.save(commit=False)           
        vehiculo = Vehiculo.objects.get(pk=form.vehiculo.id)
        vehiculo.disponible=False
        vehiculo.save()        
        form.save()
        user = form.chofer
        noti = Notificacion()
        noti.titulo = "Movimiento creado"
        noti.mensaje = "Se creo un nuevo movimiento"
        noti.modelo = "Movimiento"
        noti.idproblema = form.id
        noti.usuario_id = user.id
        noti.save()

        try:
            print("mandar notificacion de cobertura")
            notifications.sendNotification("Movimiento creado", "Se creo un nuevo movimiento", user.notification_token, user.email, noti)
        except:
            print("No se pudo enviar notificacion")
            
        try:
            print("mandar notificacion por planta")
            notifications.sendemailsbyplanta("Movimiento creado", "Se creo un nuevo movimiento", form.planta, "ddmanagement", noti)
        except Exception as error2:
            print("No se pudo enviar notificacion: "+str(error2))

        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books

        till = dt.date.today()
        if till.month == 1:
            fr = till.replace(month = 12, year = till.year - 1)
        else:
            fr = till.replace(month = till.month - 1)

        incidentes = Incidente.objects.filter(fecha__range=[fr,till])
        tipo_incidentes = TipoIncidente.objects.all()

        context['incidentes'] = incidentes
        context['tipoincidentes'] = tipo_incidentes
        context['css_list'] = css_list
        context['js_list'] = js_list        
        return context
    
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.object = None
        form = form_class(request=request)
        return self.render_to_response(self.get_context_data(form=form))
    
def admin_movimientos(request):    
    """
    Nota: Los roles que pueden acceder a la información de movimientos son los siguientes:
    
    * administrador, gerente_operativo, monitorista
    
    administrador y monitorista tienen acceso a los movimientos de cualquer planta y cualquier cliente.
    
    gerente_operativo tiene acceso a los movimientos relacionados a la planta en la que está referido su usuario
    
    """
    
    roles = ['administrador', 'gerente_operativo', 'monitorista']
    
    roleUsuario = request.user.role.alias_rol
    
    acceso = permiso(roles, roleUsuario)    
    
    plantaGteOper = request.user.planta
    
    if roleUsuario == 'monitorista':    
        movimientos = Movimiento.objects.filter(planta=plantaGteOper).all().order_by('-id')
    else:
        movimientos = Movimiento.objects.all().order_by('-id')

    return render(request, 'administrador/ddmanagement/movimientos_lista.html', { 'css_list': css_list, 'js_list': js_list, 'movimientos': movimientos, 'acceso': acceso })

class MovimientoDetail(DetailView):
    model = Movimiento
    template_name = 'administrador/ddmanagement/movimiento_detail.html'
    
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        movimiento = Movimiento.objects.get(pk=self.object.id)       
                
        return super(MovimientoDetail, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #quito js_gps_new
        js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox', 'js_gps_new']
        context['css_list'] = css_list
        context['js_list'] = js_list
        context['notificaciones'] = n 
        tickets = self.object.movimiento_tickets.all()
        context['tickets'] = tickets

        incidentes = self.object.incidentevial_set.all()
        context['incidentes'] = incidentes
        
        return context

class MovimientoUpdate(UpdateView):
    model = Movimiento
    form_class = MovimientoForm
    template_name = 'administrador/ddmanagement/movimiento_update_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_movimientos_update', args=[self.object.id]) + '?ok'

    def form_valid(self, form):

        for fieldname in form.changed_data:
            print(fieldname)
            print("old=%s" % form.initial[fieldname])
            print("new=%s" % form.cleaned_data[fieldname])
            if fieldname == "waypoints":
                chofer = form.cleaned_data['chofer']
                user = chofer
                noti = Notificacion()
                noti.titulo = "Se realizo un cambio de ruta"
                noti.mensaje = "Se actualizo la ruta del movimiento"
                noti.modelo = "Movimiento"
                noti.idproblema = self.kwargs['pk']
                noti.usuario_id = chofer.id
                noti.save()

                try:
                    print("mandar notificacion")
                    notifications.sendNotification("Se realizo un cambio de ruta", "Se actualizo la ruta del movimiento", user.notification_token, user.email, noti)
                except:
                    print("No se pudo enviar notificacion")

                try:
                    print("mandar notificacion")
                    notifications.sendemailsbyplanta("Se realizo un cambio de ruta", "Se actualizo la ruta del movimiento", form.cleaned_data['planta'], "ddmanagement", noti)
                except Exception as error2:
                    print("No se pudo enviar notificacion: "+str(error2))

            if fieldname == "ef":
                if form.cleaned_data['ef']:
                    chofer = form.cleaned_data['chofer']
                    user = chofer
                    noti = Notificacion()
                    noti.titulo = "Movimiento finalizado"
                    noti.mensaje = "El movimiento ha sido marcado como finalizado"
                    noti.modelo = "Movimiento"
                    noti.idproblema = self.kwargs['pk']
                    noti.usuario_id = chofer.id
                    noti.save()

                    try:
                        print("mandar notificacion de movimiento finalizado")
                        notifications.sendNotification("Movimiento finalizado", "El movimiento ha sido marcado como finalizado", user.notification_token, user.email, noti)
                    except:
                        print("No se pudo enviar notificacion")

                    try:
                        print("mandar notificacion por planta")
                        notifications.sendemailsbyplanta("Movimiento finalizado", "El movimiento ha sido marcado como finalizado", form.cleaned_data['planta'], "ddmanagement", noti)
                    except Exception as error2:
                        print("No se pudo enviar notificacion: "+str(error2))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context




class MovimientoDelete(DeleteView):
    model = Movimiento
    success_url = reverse_lazy('administrador:admin_movimientos_lista')
    template_name = 'administrador/ddmanagement/movimiento_confirm_delete.html'

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context    
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        vehiculo = self.object.vehiculo        
        vehiculo.disponible=True
        vehiculo.save()
        return super(MovimientoDelete, self).delete(*args, **kwargs)
        
class VehiculoCrete(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'administrador/ddmanagement/vehiculo_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_vehiculos_lista') + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def admin_vehiculos(request):

    vehiculos = Vehiculo.objects.all()

    return render(request, 'administrador/ddmanagement/vehiculos_lista.html', { 'css_list': css_list, 'js_list': js_list, 'vehiculos': vehiculos })

class VehiculoDetail(DetailView):
    model = Vehiculo
    template_name = 'administrador/ddmanagement/vehiculo_detail.html'

    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class VehiculoUpdate(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'administrador/ddmanagement/vehiculo_update_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:admin_vehiculos_update', args=[self.object.id]) + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class VehiculoDelete(DeleteView):
    model = Vehiculo
    success_url = reverse_lazy('administrador:admin_vehiculo_lista')
    template_name = 'administrador/ddmanagement/vehiculo_confirm_delete.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def mapa_geocercas(request, pk):

    planta = Planta.objects.get(pk=pk)
    guardias = planta.user_set.filter(role__alias_rol="guardia")

    return render(request, 'administrador/zona0/geocercas_plantas.html', { 'css_list': css_list, 'js_list': js_list, 'planta': planta, 'guardias': guardias})

def ajax_last_tracking(request):

    print("request planta "+str(request.GET.get('planta_id')))
    planta = Planta.objects.get(pk=request.GET.get('planta_id'))
    guardias = planta.user_set.all()
    sjson = []
    for guardia in guardias:
        sjson.append({"guardia": str(guardia.first_name)+" "+str(guardia.last_name),"guardia_id": guardia.id, "fecha": guardia.getLastTracking().fecha, "lat": guardia.getLastTracking().lat, "lng": guardia.getLastTracking().lng})

    return JsonResponse(sjson, safe=False)

def admin_asistencias(request):
    
    ClientFilter = "OFICINAS CENTRALES MATRIX"
    asistencias = CiaaR1.objects.filter(cliente=ClientFilter)

    return render(request, 'administrador/predictive/asistencias.html', { 'css_list': css_list, 'js_list': js_list, 'asistencias': asistencias })

class generate_pdf_analisis_riesgo(View):       
    
    def post(self, request, *args, **kwargs):                     
        cliente = request.POST.get('cliente')                                    
        planta = request.POST.get('planta')  
        p_ids = request.POST.get('p_ids') 
        j = json.loads(p_ids)

        idsarray = []

        print(j)
        for item in j:
            print("id "+str(item))
            idsarray.append(item)

        format = "%Y-%m-%d"

        fecha = date.today()

        fecha = fecha.strftime(format)

        recomendaciones = Recomendacion.objects.filter(papeleta_id__in=idsarray).all()
        print(recomendaciones)

        #fechalevantamiento = recomendaciones[0].papeleta.fecha

        #fechalevantamiento = fechalevantamiento.strftime(format)

        recomendacionesControlAccesos = recomendaciones.filter(papeleta_id__encuesta_id__nombre="CONTROL DE ACCESOS")

        recomendacionesInteriorEdificio = recomendaciones.filter(papeleta_id__encuesta_id__nombre="INTERIOR DEL EDIFICIO")

        recomendacionesLogistica = recomendaciones.filter(papeleta_id__encuesta_id__nombre="LOGISTICA")

        recomendacionesAlarma = recomendaciones.filter(papeleta_id__encuesta_id__nombre="ALARMAS")

        recomendacionesCCTV = recomendaciones.filter(papeleta_id__encuesta_id__nombre="CCTV")

        recomendacionesMurosPerimetrales = recomendaciones.filter(papeleta_id__encuesta_id__nombre="MUROS PERIMETRALES")

        recomendacionesEntorno = recomendaciones.filter(papeleta_id__encuesta_id__nombre="ENTORNO")

        recomendacionesEmbarqueInterior = recomendaciones.filter(papeleta_id__encuesta_id__nombre="EMBARQUE INTERIOR")

        recomendacionesEmbarqueExterior = recomendaciones.filter(papeleta_id__encuesta_id__nombre="EMBARQUE EXTERIOR")

        recomendacionesProcedimientos = recomendaciones.filter(papeleta_id__encuesta_id__nombre="PROCEDIMIENTOS")

        recomendacionesRecursosHumanos = recomendaciones.filter(papeleta_id__encuesta_id__nombre="RECURSOS HUMANOS")      

        img = '%s' % (request.POST.get('img'))  
        img2 = '%s' % (request.POST.get('img2'))  
        img3 = '%s' % (request.POST.get('img3'))  
        img4 = '%s' % (request.POST.get('img4'))
        img5 = '%s' % (request.POST.get('img5'))  
        img6 = '%s' % (request.POST.get('img6'))  
        img7 = '%s' % (request.POST.get('img7'))  
       
        user = request.user.username
        userId = str(request.user.id)        
        path = 'media/avatars/'+user+userId
        a= path
        path=str(path)
        
        if os.path.exists(path):
            shutil.rmtree(path)

        os.mkdir(path)
        nombre =  path + '/image.png'
        nombre2 =  path + '/image2.png'
        nombre3 =  path + '/image3.png'
        nombre4 =  path + '/image4.png'
        nombre5 =  path + '/image5.png'
        nombre6 =  path + '/image6.png'
        nombre7 =  path + '/image7.png'
        
        setCliente = Cliente.objects.get(pk=cliente)
        if planta != "":
            setPlanta = Planta.objects.get(pk=planta)        
        else: 
            setPlanta = "none"
            
        data = base64.b64decode(img)        
        im = Image.open(BytesIO(data))  
        im.save(nombre, 'PNG')
        
        data2 = base64.b64decode(img2)        
        im2 = Image.open(BytesIO(data2))  
        im2.save(nombre2, 'PNG')
        
        data3 = base64.b64decode(img3)        
        im3 = Image.open(BytesIO(data3))  
        im3.save(nombre3, 'PNG')
        
        data4 = base64.b64decode(img4)        
        im4 = Image.open(BytesIO(data4))  
        im4.save(nombre4, 'PNG')
        
        data5 = base64.b64decode(img5)        
        im5 = Image.open(BytesIO(data5))  
        im5.save(nombre5, 'PNG')
        
        data6 = base64.b64decode(img6)        
        im6 = Image.open(BytesIO(data6))  
        im6.save(nombre6, 'PNG')
        
        data7 = base64.b64decode(img7)        
        im7 = Image.open(BytesIO(data7))  
        im7.save(nombre7, 'PNG')


        
        sjson = {
            "papeletas": "None",
            "recomendaciones_count": recomendaciones.count(),
            "recomendaciones": recomendaciones,
            "v_infraestructura": "None",
            "r_infraestructura": "None",
            "v_seguridad_operativa": "None",
            "r_seguridad_operativa": "None",
            "v_seguridad_electronica": "None",
            "r_seguridad_electronica": "None",
            "v_logistica": "None",
            "r_logistica": "None",
            "v_entorno": "None",
            "r_entorno": "None",
            "cat_infraestructura": "None",
            "cat_infraestructura_avg": "None",
            "cat_seg_operativa": "None",
            "cat_seg_operativa_avg": "None",
            "cat_seg_electrica": "None",
            "cat_seg_electrica_avg": "None",
            "cat_logistica": "None",
            "cat_logistica_avg": "None",
            "cat_entorno": "None",
            "cat_entorno_avg": "None",
            "clientes": "None",
            "plantas": "None",
            "papeletas_2": "None",
            "controlAccesos": recomendacionesControlAccesos,
            "interiorEdificio": recomendacionesInteriorEdificio,
            "logistica": recomendacionesLogistica,
            "alarma": recomendacionesAlarma,
            "cctv": recomendacionesCCTV,
            "murosPerimetrales": recomendacionesMurosPerimetrales,
            "entorno": recomendacionesEntorno,
            "embarqueInterior": recomendacionesEmbarqueInterior,
            "embarqueExterior": recomendacionesEmbarqueExterior,
            "procedimientos": recomendacionesProcedimientos,
            "recursosHumanos": recomendacionesRecursosHumanos,
            "fecha": fecha,
            #"fechalevantamiento": fechalevantamiento,
            "cliente": setCliente,
            "planta": setPlanta,
            "img1": nombre,
            "img2": nombre2,
            "img3": nombre3,
            "img4": nombre4,
            "img5": nombre5,
            "img6": nombre6,
            "img7": nombre7
        }      

        print(sjson)            
        
        pdf = render_to_pdf('administrador/pdfs/analisis-de-riesgo-test.html', sjson)                         
        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
        #filename = "Analisis-de-riesgo.pdf"
        #content = "inline; filename='%s'" %(filename)               
        #content = "attachment; filename=%s" %(filename)            
        #response['Content-Disposition'] = content    
        #shutil.rmtree(a)         
        #    return response
            return response

        return HttpResponse("Not found")  

class generate_pdf_predictive(View):
     def post(self, request, *args, **kwargs):                     
        
        format='png'
        img = request.POST.get('img')    
        img2 = request.POST.get('img2')    
        img3 = request.POST.get('img3')    
        img4 = request.POST.get('img4')    
        img5 = request.POST.get('img5')    
        img6 = request.POST.get('img6')  
        img7 = request.POST.get('img7')  
        img8 = request.POST.get('img8')  
        img9 = request.POST.get('img9')  
        img10 = request.POST.get('img10')  
        img11 = request.POST.get('img11')  
        img12 = request.POST.get('img12')  
        img13 = request.POST.get('img13')  
        img14 = request.POST.get('img14')  

        

        #cliente = request.POST.get('cliente')                                          
        img = '%s' % (img)  
        img2 = '%s' % (img2)  
        img3 = '%s' % (img3)  
        img4 = '%s' % (img4)
        img5 = '%s' % (img5)  
        img6 = '%s' % (img6)  
        img7 = '%s' % (img7)  
        img8 = '%s' % (img8)  
        img9 = '%s' % (img9)  
        img10 = '%s' % (img10)  
        img11 = '%s' % (img11)  
        img12 = '%s' % (img12)  
        img13 = '%s' % (img13)  
        img14 = '%s' % (img14)  

        dominioLocal = 'C:/Users/ASI WE2/Documents/proyecto/13/Panoptic-Server-master' 
        dominioRemoto = '/home/ubuntu/pgit'

        user = request.user.username
        hi = request.user.id
        
        path = dominioRemoto +'/media/avatars/'+user

        a= path
        path=str(path)        
        os.mkdir(path)

        nombre = path + '/imaged.png'
        nombre2 =  path + '/imagef.png'
        nombre3 =  path + '/imaget.png'
        nombre4 =  path + '/imagey.png'
        nombre5 =  path + '/imageu.png'
        nombre6 =  path + '/imagei.png'
        nombre7 =  path + '/imagee.png'
        nombre8 =  path + '/imagea.png'
        nombre9 =  path + '/image8.png'
        nombre10 =  path + '/image58.png'
        nombre11 =  path + '/image55.png'
        nombre12 =  path + '/image98.png'
        nombre13 =  path + '/image52.png'
        nombre14 =  path + '/image463.png'
        
        data = base64.b64decode(img)        
        im = Image.open(BytesIO(data))  
        im.save(nombre, 'PNG')
        
        data2 = base64.b64decode(img2)        
        im2 = Image.open(BytesIO(data2))  
        im2.save(nombre2, 'PNG')
        
        data3 = base64.b64decode(img3)        
        im3 = Image.open(BytesIO(data3))  
        im3.save(nombre3, 'PNG')
        
        data4 = base64.b64decode(img4)        
        im4 = Image.open(BytesIO(data4))  
        im4.save(nombre4, 'PNG')
        
        data5 = base64.b64decode(img5)        
        im5 = Image.open(BytesIO(data5))  
        im5.save(nombre5, 'PNG')
        
        data6 = base64.b64decode(img6)        
        im6 = Image.open(BytesIO(data6))  
        im6.save(nombre6, 'PNG')

        data7 = base64.b64decode(img7)        
        im7 = Image.open(BytesIO(data7))  
        im7.save(nombre7, 'PNG')
        
        data8 = base64.b64decode(img8)        
        im8 = Image.open(BytesIO(data8))  
        im8.save(nombre8, 'PNG')

        data9 = base64.b64decode(img9)        
        im9 = Image.open(BytesIO(data9))  
        im9.save(nombre9, 'PNG')

        data10 = base64.b64decode(img10)        
        im10 = Image.open(BytesIO(data10))  
        im10.save(nombre10, 'PNG')

        data11 = base64.b64decode(img11)        
        im11 = Image.open(BytesIO(data11))  
        im11.save(nombre11, 'PNG')

        data12 = base64.b64decode(img12)        
        im12 = Image.open(BytesIO(data12))  
        im12.save(nombre12, 'PNG')

        data13 = base64.b64decode(img13)        
        im13 = Image.open(BytesIO(data13))  
        im13.save(nombre13, 'PNG')

        data14 = base64.b64decode(img14)        
        im14 = Image.open(BytesIO(data14))  
        im14.save(nombre14, 'PNG')

        sjson = {
            "papeletas": "None",
            "v_infraestructura": "None",
            "r_infraestructura": "None",
            "v_seguridad_operativa": "None",
            "r_seguridad_operativa": "None",
            "v_seguridad_electronica": "None",
            "r_seguridad_electronica": "None",
            "v_logistica": "None",
            "r_logistica": "None",
            "v_entorno": "None",
            "r_entorno": "None",
            "cat_infraestructura": "None",
            "cat_infraestructura_avg": "None",
            "cat_seg_operativa": "None",
            "cat_seg_operativa_avg": "None",
            "cat_seg_electrica": "None",
            "cat_seg_electrica_avg": "None",
            "cat_logistica": "None",
            "cat_logistica_avg": "None",
            "cat_entorno": "None",
            "cat_entorno_avg": "None",
            "clientes": "None",
            "plantas": "None",
            "papeletas_2": "None",
            "img1": nombre,
            "img2": nombre2,
            "img3": nombre3,
            "img4": nombre4,
            "img5": nombre5,
            "img6": nombre6,
            "img7": nombre7,
            "img8": nombre8,
            "img9": nombre9,
            "img10": nombre10,
            "img11": nombre11,
            "img12": nombre12,
            "img13": nombre13,
            "img14": nombre14,
        }                  
        
        pdf = render_to_pdf('administrador/pdfs/predictive.html', sjson)                         

        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Analisis-de-riesgo.pdf"
            content = "inline; filename='%s'" %(filename)               
            content = "attachment; filename=%s" %(filename)            
            response['Content-Disposition'] = content 
            shutil.rmtree(a)           
            return response
        
        return HttpResponse("Not found")    
        
def getAVGVul(encuestas_names, cat):
    tempArray = []
    for name in encuestas_names:
        num = 0
        total = 0
        totalr = 0
        avg = 0
        avgr = 0
        for e in cat:
            if name == e["nombre"]:
                num += 1
                total += e["vul"]
                totalr += e["riesgo"]

        if num > 0:
            jsonTemp = {"nombre": name, "total": total, "totalr": totalr, "avg": (total/num), "avgr": (totalr/num) }
            tempArray.append(jsonTemp)

    return tempArray;

def filterEncuestas(papeletas):
    #get distings plantas
    plantas_ids = []
    for p in papeletas:
        if p.planta_id not in plantas_ids:
            plantas_ids.append(p.planta_id)
            print("agregada Planta "+str(p.planta_id))


    pencuestas = []
    pencuestas_ids = []
    p_ids = []
    #for each planta
    for pid in plantas_ids:
        print("evaluando Planta "+str(pid))
        pfiltered = papeletas.filter(planta_id=pid)
        #each papelete in planta
        
        pencuestas_ids = []
        #tomar encuesta mas reciente de cada una diferente
        for penc in pfiltered.order_by("encuesta_id", "-fecha"):
            print("evaluando "+str(penc.encuesta_id))
            if penc.encuesta_id not in pencuestas_ids:
                pencuestas.append(penc)
                print("papeleta "+str(penc.id))
                p_ids.append(penc.id)
                pencuestas_ids.append(penc.encuesta_id)
                print("agregada "+str(penc))
            
    print("pids "+str(p_ids))
    print("enc_ids "+str(pencuestas_ids))
    print("papeletas "+str(pencuestas))
    #papeletas filtradas por la mas recientes de cada tipo
    papeletas = papeletas.filter(id__in=p_ids).all()

    return papeletas
    
def ajax_get_notificaciones(request):    
    
    #start = dt.date.today()
    
    #notificaciones = request.user.notificacion_set.filter(fecha__date=start).order_by('-fecha').all()
    
    notificaciones = request.user.notificacion_set.order_by('-fecha').all()
    return render(request, 'administrador/options/lista_de_notificaciones.html', {'notificaciones': notificaciones })
