from django.shortcuts import render, HttpResponse, redirect, get_list_or_404, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView, RequestConfig, tables
from django.urls import reverse, reverse_lazy
from .models import *
from core.models import Planta, Cliente, User, Role
from .tables import RondinTable, PuntoTable
from .forms import RondinForm, PuntoForm
from core import user_validation
from datetime import datetime, date, time, timedelta
from django.db.models import Avg, Max, Min, Sum
from core import notifications

from django.http import JsonResponse, HttpResponse
from analytics.models import F_ES_Trailers, F_18_puntos_Trailer, F_Visitantes, EntradaVehiculo, Paqueteria, ItemEntradaMaterial, Area_Restringida, Empleado_Sin_Gafete, ItemEntradaEquipo, RecibosAlmacen, Incidentes, RondinHecho
from django.core import serializers
from django.db.models import Sum
from django.db.models import Q
from django.utils import timezone
import datetime as dt
import pytz

# Create your views here.
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']


def homeold(request):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = None
    #print("from view: "+str(userdict))
    request.session['django_plotly_dash'] = dash_context

    return render(request, "analytics/home.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict})

def home(request):

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = None
    #print("from view: "+str(userdict))
    request.session['django_plotly_dash'] = dash_context

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

    return render(request, "analytics/home2.html", { 'css_list': css_list, 'js_list': js_list, 'vcliente': cliente, 'vplantas': plantas })


def home_planta(request, id):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']

    print(id)

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = id
    request.session['django_plotly_dash'] = dash_context

    return render(request, "analytics/home.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict})
    
def rondines_dashboard(request):
    cliente = request.user.cliente
    rondines = Rondin.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    rondineshechos = RondinHecho.objects.none()
    for r in rondines:
        if rondineshechos.all().count() == 0:
            rondineshechos = r.rondin_rondinhecho.all()
        else:
            if r.rondin_rondinhecho.all().count() > 0:
                rondineshechos.union(r.rondin_rondinhecho.all())

    return render(request, "analytics/rondin_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'rondines': rondines, 'rondineshechos': rondineshechos})

def rondinhecho(request, id):
    rondinhecho = RondinHecho.objects.get(id=id)
    userdict = user_validation.validate(request)

    return render(request, "analytics/rondinhecho_detalle.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'rondinhecho': rondinhecho})

def fvisitantes_dashboard(request):
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    visitantes = F_Visitantes.objects.none()
    for p in plantas:
        if visitantes.all().count() == 0:
            visitantes = p.planta_fvisitante.all()
        else:
            if p.planta_fvisitante.all().count() > 0:
                visitantes.union(p.planta_fvisitante.all())

    return render(request, "analytics/visitantes_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'plantas': plantas, 'visitantes': visitantes})

def fvisitantes_detail(request, pk):    
    visitante = F_Visitantes.objects.get(pk=pk)

    try:
        vehiculo = EntradaVehiculo.objects.get(visitante=visitante)
    except Exception:
        vehiculo = None

    try:
        equipos = EntradaEquipo.objects.get(visitante=visitante)
    except Exception:
        equipos = None

    try:
        ItemsEquipos = ItemEntradaEquipo.objects.filter(entradaequipo_id=equipos.id)
    except Exception:
        ItemsEquipos = None

    try:
        materiales = EntradaMateriales.objects.get(visitante=visitante)
    except Exception:
        materiales = None   
        
    try:
        ItemsMateriales = ItemEntradaMaterial.objects.filter(entradamateriales_id=materiales.id)    
    except Exception:
        ItemsMateriales = None  
    
    return render(request, 'analytics/visitantes_detail.html', { 'css_list': css_list, 'js_list': js_list, 'visitante': visitante, 'vehiculo': vehiculo, 'equipos': equipos, 'ItemsEquipos':ItemsEquipos, 'materiales': materiales, 'ItemsMateriales': ItemsMateriales })

def empleadossingafete_dashboard(request):
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    empleados = Empleado_Sin_Gafete.objects.none()
    for p in plantas:
        if empleados.all().count() == 0:
            empleados = p.planta_empleadosingafete.all()
        else:
            if p.planta_empleadosingafete.all().count() > 0:
                empleados.union(p.planta_empleadosingafete.all())

    return render(request, "analytics/empleadossingafete_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'plantas': plantas, 'empleados': empleados})

def arearestringida_dashboard(request):
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    accesos = Area_Restringida.objects.none()
    for p in plantas:
        if accesos.all().count() == 0:
            accesos = p.planta_arearestringida.all()
        else:
            if p.planta_arearestringida.all().count() > 0:
                accesos.union(p.planta_arearestringida.all())

    return render(request, "analytics/arearestringida_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'plantas': plantas, 'accesos': accesos})

def recibos_dashboard(request):
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    recibos = RecibosAlmacen.objects.none()
    for p in plantas:
        if recibos.all().count() == 0:
            recibos = p.planta_recibos.all()
        else:
            if p.planta_recibos.all().count() > 0:
                recibos.union(p.planta_recibos.all())

    return render(request, "analytics/recibos_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'plantas': plantas, 'recibos': recibos})

def recibos_detail(request, pk):
    recibos = RecibosAlmacen.objects.get(pk=pk)
    recibos_items = RecibosItems.objects.filter(recibo_id=recibos.id) 
    
    return render(request, 'analytics/recibos_detail.html', { 'css_list': css_list, 'js_list': js_list, 'recibos': recibos, 'recibos_items': recibos_items})  

def recibos_detail(request, pk):
    recibos = RecibosAlmacen.objects.get(pk=pk)
    recibos_items = RecibosItems.objects.filter(recibo_id=recibos.id) 
    
    return render(request, 'analytics/recibos_detail.html', { 'css_list': css_list, 'js_list': js_list, 'recibos': recibos, 'recibos_items': recibos_items})  

def paqueteria_dashboard(request):
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente_id=cliente.id)
    userdict = user_validation.validate(request)
    paquetes = Paqueteria.objects.none()
    for p in plantas:
        if paquetes.all().count() == 0:
            paquetes = p.planta_paqueteria.all()
        else:
            if p.planta_paqueteria.all().count() > 0:
                paquetes.union(p.planta_paqueteria.all())

    return render(request, "analytics/paqueteria_dashboard.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'plantas': plantas, 'paquetes': paquetes})

def paqueteria_detail(request, pk):
    paqueterias = Paqueteria.objects.get(pk=pk) 
    return render(request, 'analytics/paqueteria_detail.html', { 'css_list': css_list, 'js_list': js_list, 'paqueterias': paqueterias })  

class RondinesList(SingleTableView):
    model = Rondin
    table_class = RondinTable
    template_name = 'analytics/list_rondines.html'

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Rondin.objects.filter(nombre__contains=query)
        else:
            lista = Rondin.objects.all()
        return lista


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class RondinCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Rondin
    form_class = RondinForm

    def get_success_url(self):
        return reverse_lazy('analytics:list_rondines')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

def ajax_load_plantas(request):
    cliente_id = request.GET.get('cliente')
    plantas = Planta.objects.filter(cliente_id=cliente_id).order_by('nombre')
    return render(request, 'analytics/options/planta_dropdown_options.html', {'plantas': plantas})

class RondinUpdate(UpdateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Rondin
    form_class = RondinForm

    def get_success_url(self):
        return reverse_lazy('analytics:list_rondines')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class RondinDetail(DetailView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Rondin
    form_class = RondinForm
    
    def get_context_data(self, **kwargs):
        puntos = self.object.punto_set.all()
        table = PuntoTable(puntos)
        RequestConfig(self.request, paginate=False).configure(table)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['table'] = table
        context['pk'] = self.kwargs.get("pk")
        return context

class RondinDelete(DeleteView):
    model = Rondin
    success_url = reverse_lazy('analytics:list_rondines')

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class PuntoCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Punto
    form_class = PuntoForm

    def get_success_url(self):
        return reverse_lazy('analytics:detail_rondin', kwargs={'pk': self.kwargs.get("pk")} )

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.rondin = Rondin.objects.get(pk=self.kwargs.get("pk"))

        form.save()
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['pk'] = self.kwargs.get("pk")
        return context

class PuntoUpdate(UpdateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Punto
    form_class = PuntoForm

    def get_success_url(self):
        return reverse_lazy('analytics:detail_rondin',  kwargs={'pk': self.object.rondin_id} )
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['pk'] = self.kwargs.get("pk")
        return context

def estados_fuerza(request):    
    #revisiones = F_18_puntos_Trailer.objects.all()   
    plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
    clientes = Cliente.objects.filter(id=request.user.cliente_id).all()

    return render(request, 'analytics/estados-fuerza.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes})


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


    return render(request, 'analytics/estados-fuerza_ajax.html', {"estadosfuerza": estadosfuerza, "planta": planta, 'faltas': faltas, 'bajas': bajas, 'vacantes': vacantes, 'inicio': inicio, 'fin': fin, "turnos": turnos, 'cubiertos': cubiertos, 'cobertura': cobertura})

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
        fuerza.no_orden = request.POST.get("no_orden")
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

        return redirect('analytics:estados_fuerza')
    
    return render(request, 'analytics/estados-fuerza_create.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "roles": roles, 'sucursales': sucursales })

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
        fuerza.no_orden = request.POST.get("no_orden")
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

        return redirect('analytics:estados_fuerza')
    
    return render(request, 'analytics/estados-fuerza_edit.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "roles": roles, 'sucursales': sucursales, 'fuerza': fuerza })

class EstadoFuerzaDelete(DeleteView):
    model = EstadoFuerza
    success_url = reverse_lazy('administrador:admin_estados_fuerza')
    template_name = 'analytics/estadofuerza_confirm_delete.html'

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

        return redirect('analytics:estados_fuerza')

    return render(request, 'analytics/estado_fuerza_cobertura_create.html', {'css_list': css_list, 'js_list': js_list, 'estadofuerza': estadofuerza, 'cobertura': cobertura})

def falta_list(request):

    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        faltas = Falta.objects.all()
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        faltas = Falta.objects.filter(planta__in=plantas).all()
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        faltas = Falta.objects.filter(planta__in=plantas).all()

    return render(request, 'analytics/faltas.html', { 'css_list': css_list, 'js_list': js_list, 'faltas': faltas })

def baja_list(request):
    
    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        bajas = Baja.objects.all()
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        bajas = Baja.objects.filter(planta__in=plantas).all()
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        bajas = Baja.objects.filter(planta__in=plantas).all()

    return render(request, 'analytics/bajas.html', { 'css_list': css_list, 'js_list': js_list, 'bajas': bajas })

def vacante_list(request):
    
    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        vacantes = Vacante.objects.all()
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        vacantes = Vacante.objects.filter(planta__in=plantas).all()
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        vacantes = Vacante.objects.filter(planta__in=plantas).all()

    return render(request, 'analytics/vacantes.html', { 'css_list': css_list, 'js_list': js_list, 'vacantes': vacantes })

def es_trailers_dashboard(request):
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id'))    
    estrailers = F_ES_Trailers.objects.all()    
    
    return render(request, 'analytics/es-trailers-historial.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'estrailers': estrailers })

def es_trailers_detail(request, pk):
    
    estrailer = F_ES_Trailers.objects.get(pk=pk)

    return render(request, 'analytics/es-trailers-ver.html', { 'css_list': css_list, 'js_list': js_list, 'estrailer': estrailer })

def logros_dashboard(request):
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id'))    
    logros = Logro.objects.all()    
    
    return render(request, 'analytics/logro_list.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'logros': logros })

def logros_detail(request, pk):
    
    logros = Logro.objects.get(pk=pk)

    return render(request, 'analytics/logro_detail.html', { 'css_list': css_list, 'js_list': js_list, 'logros': logros })


def predictive_analytics_dashboard(request):  
    #Verifica que esté definido vcliene 
    cliente = request.user.cliente    
    if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
        plantas = Planta.objects.filter(cliente=cliente)
    else:
        nombreplanta = request.user.planta       
        plantas = Planta.objects.filter(nombre=nombreplanta)

    #return render(request, 'administrador/predictive/admin_predictive_analytics.html', { 'css_list': css_list, 'js_list': js_list 
    return render(request, 'analytics/dashboard.html', { 'css_list': css_list, 'js_list': js_list, 'vcliente': cliente, 'vplantas': plantas })




#### AJAX Dashboard Frontend Predictive Analytics ####
def ajax_charts_numero_entradas_salidas_trailers(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)
    
    dias=[]
    entradas=[]
    salidas=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            entrada = F_ES_Trailers.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            entradas.append(entrada)    
                        
            salida = F_ES_Trailers.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            salidas.append(salida) 
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            entrada = F_ES_Trailers.objects.filter(entrada__date=start).count()
            entradas.append(entrada) 
            
            salida = F_ES_Trailers.objects.filter(salida__date=start).count()
            salidas.append(salida) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "entradas": entradas,
    "salidas": salidas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_revision_18_puntos(request):    
    planta = request.GET.get('planta')
    field = request.GET.get('tincidente')    
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date()     
    lookup = "%s__isnull" % field             
    delta = dt.timedelta(days=1)
    
    dias=[]
    incidentes=[]

    print(field)
    print(lookup)
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            incidente = F_18_puntos_Trailer.objects.filter(planta=objPlanta).filter(fecha__date=start).exclude(**{ lookup: True}).count()
            
            incidentes.append(incidente)    
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            incidente = F_18_puntos_Trailer.objects.filter(fecha__date=start).exclude(**{ lookup: True}).count()
            incidentes.append(incidente) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "incidentes": incidentes
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_registro_visitantes(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    visitantes=[]
    proveedores=[]
    contratistas=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            visitante = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo='visitante').count()
            visitantes.append(visitante)    
                        
            proveedor = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo="proveedores").count()
            proveedores.append(proveedor) 

            contratista = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo='contratista').count()
            contratistas.append(contratista) 
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            visitante = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='visitante').count()
            visitantes.append(visitante) 
            
            proveedor = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='proveedores').count()
            proveedores.append(proveedor) 

            contratista = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='contratista').count()
            contratistas.append(contratista) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "visitantes": visitantes,
    "proveedores": proveedores,
    "contratistas": contratistas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_registro_vehiculos(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    vehiculos=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            vehiculo = EntradaVehiculo.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            vehiculos.append(vehiculo)    
                        
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            vehiculo = EntradaVehiculo.objects.filter(fecha__date=start).count()
            vehiculos.append(vehiculo) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "vehiculos": vehiculos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_paquetes_dañados(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    paquetes=[]
    danados=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            paquete = Paqueteria.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            paquetes.append(paquete)   

            danado =  Paqueteria.objects.filter(planta=objPlanta).filter(fecha__date=start).filter( Q(bolcables='1')  | Q(bolfaltainfo= '1') | Q(bolfuerahorario='1') | Q(bololor='1') | Q(bolpolvo='1') ).count()
            danados.append(danado)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            paquete = Paqueteria.objects.filter(fecha__date=start).count()
            paquetes.append(paquete) 

            danado = Paqueteria.objects.filter(fecha__date=start).filter( Q(bolcables='1')  | Q(bolfaltainfo= '1') | Q(bolfuerahorario='1') | Q(bololor='1') | Q(bolpolvo='1') ).count()
            danados.append(danado)
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "paquetes": paquetes,
    "danados": danados
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_materiales(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    materiaprimas=[]
    quimicos=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            materiaprima = ItemEntradaMaterial.objects.filter(planta=objPlanta).filter(entradamateriales_id__fecha__date=start).filter(tipo='materia prima').count()
            materiaprimas.append(materiaprima)   

            quimico =  ItemEntradaMaterial.objects.filter(planta=objPlanta).filter(entradamateriales_id__fecha__date=start).filter(tipo="quimico").count()
            quimicos.append(quimico)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            materiaprima = ItemEntradaMaterial.objects.filter(entradamateriales_id__fecha__date=start).filter(tipo='materia prima').count()
            materiaprimas.append(materiaprima) 

            quimico = ItemEntradaMaterial.objects.filter(entradamateriales_id__fecha__date=start).filter(tipo="quimico").count()
            quimicos.append(quimico)
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "materia prima": materiaprimas,
    "quimicos": quimicos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_areas_restingida(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    entradas=[]
    
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            entrada = Area_Restringida.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            entradas.append(entrada)   

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            entrada = Area_Restringida.objects.filter(fecha__date=start).count()
            entradas.append(entrada) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "entradas": entradas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_empleado_sin_gafete(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    vehiculares=[]
    personales=[]
    ambos=[]

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            vehicular = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetevehicular='1').filter(bolgafetepersonal='0').count()
            vehiculares.append(vehicular)

            personal = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='0').count()
            personales.append(personal)

            ambo = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='1').count()
            ambos.append(ambo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            vehicular = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetevehicular='1').filter(bolgafetepersonal='0').count()
            vehiculares.append(vehicular) 
            
            personal = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='0').count()
            personales.append(personal) 

            ambo = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='1').count()
            ambos.append(ambo) 

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "vehiculares": vehiculares,
    "personales": personales,
    "ambos": ambos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_equipo(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    equipos=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            equipo = ItemEntradaEquipo.objects.filter(planta=objPlanta).filter(entradaequipo_id__fecha__date=start).count()
            equipos.append(equipo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            equipo = ItemEntradaEquipo.objects.filter(entradaequipo_id__fecha__date=start).count()
            equipos.append(equipo) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "equipos": equipos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_recibos(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    recibos=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            recibo = RecibosAlmacen.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            recibos.append(recibo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            recibo = RecibosAlmacen.objects.filter(fecha__date=start).count()
            recibos.append(recibo) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "recibos": recibos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_incidentes_servicio(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    incidentes=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            incidente = Incidentes.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            incidentes.append(incidente)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            incidente = Incidentes.objects.filter(fecha__date=start).count()
            incidentes.append(incidente) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "incidentes": incidentes
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_rondines(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)

    dias=[]
    rondines=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            rondin = RondinHecho.objects.filter(planta=objPlanta).filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            rondines.append(rondin)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            rondin = RondinHecho.objects.filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            rondines.append(rondin) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "rondines": rondines
    }
    
    return JsonResponse(to_json, safe=False)