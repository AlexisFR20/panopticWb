from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView, RequestConfig, tables
from django.urls import reverse, reverse_lazy
from .models import *
from core.models import Planta
from .tables import RondinTable, PuntoTable
from .forms import RondinForm, PuntoForm
from core import user_validation
from datetime import datetime, date, time, timedelta
from django.db.models import Avg, Max, Min, Sum
from core import notifications

# Create your views here.
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']


def home(request):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = None
    #print("from view: "+str(userdict))
    request.session['django_plotly_dash'] = dash_context

    return render(request, "analytics/home.html", {"css_list": css_list, "js_list": js_list, 'userdict': userdict})

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
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    usuarios = User.objects.all()
    estadosfuerza = EstadoFuerza.objects.all().order_by("-fecha_inicio")
    print("fuerzas "+str(estadosfuerza.count()))

    return render(request, 'analytics/estados-fuerza.html', {'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'usuarios': usuarios, "estadosfuerza": estadosfuerza})

def ajax_load_estados_fuerza(request):
    planta = Planta.objects.get(id=request.GET.get("planta_id"))
    estadosfuerza = EstadoFuerza.objects.filter(cliente_id=request.GET.get("cliente_id")).filter(planta_id=request.GET.get("planta_id")).filter(fecha_inicio__range=[request.GET.get("start"), request.GET.get("end")]).all().order_by("-fecha_inicio")
    fin = datetime.strptime(request.GET.get("end"), '%Y-%m-%d')
    while fin.weekday() != 6: #0 for monday
        fin += timedelta(days=1)
    print("end "+str(request.GET.get("end")))
    print("fin "+str(fin.date()))
    faltas = Falta.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha")
    print("faltas "+str(faltas.count()))
    bajas = Baja.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha")
    print("bajas "+str(bajas.count()))
    vacantes = Vacante.objects.filter(planta_id=request.GET.get("planta_id")).filter(fecha__range=[request.GET.get("start"), fin]).all().order_by("-fecha").aggregate(Sum('n_vacantes'))
    print(vacantes)
    return render(request, 'analytics/estados-fuerza_ajax.html', {"estadosfuerza": estadosfuerza, "planta": planta, 'faltas': faltas, 'bajas': bajas, 'vacantes': vacantes})

  
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