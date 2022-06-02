from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from core import charts
from core import dash
from django.utils.html import escape
from django.utils import timezone
from core import user_validation
from entorno.models import Incidente,  TipoIncidente
from core.models import Planta, Cliente, User, Notificacion, Ciudad
from arnes.models import Recomendacion
from analytics.models import EstadoFuerza
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View
from core.utils import render_to_pdf
from django.template.loader import get_template
from core.utils import *
import datetime

from django.db.models import Count

import feedparser
import json

n = Notificacion.objects.filter(visto = False)
r = Recomendacion.objects.all()[0:10]
def error_404_view(request, exception):    
    return render(request, 'core/errores/404.html')
    
def redirect404(request): 
    css_list = ['basic', 'slick', 'custom']
    js_list = ['js_basic', 'js_slick']        
        
    return render(request, "core/errores/404redirect.html", { 'css_list': css_list, 'js_list': js_list } )
    
def mostrar_notificacion (request, notificacion_id=None):
    if notificacion_id != None:        
        n = Notificacion.objects.get(id=notificacion_id)
        n.visto = True
    else:
        n= None
    return render_to_response({'notificacion': n})

class CustomLoginView(LoginView):
    """
    Custom login view.
    """
    def post(self, request, *args, **kwargs):            
        username = request.POST.get('username')
        password = request.POST.get('password')        
        print(username)
        print(password) 
        if not request.POST['username']:
            messages.error(request, 'Escriba su usuario por favor.')
            return redirect('login')
        
        if request.POST['password'] == 'password':
            messages.error(request, 'Tu contraseña es muy simple')
            return redirect('login')
        
        if not request.POST['password']:
            messages.error(request, 'Debe escribir su contraseña válida')
            return redirect('login')        
                        
        #u = User.objects.get(username=username) 
        # Obtiene el record de usuario a partir del username otorgado        
        try:
            u = User.objects.get(username=username) 
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('login')
       
        if check_password(password, u.password):            
            user = authenticate(username=username, password=password)
            if user is not None:
                # realiza la autenticación del usuario                 
                auth.login(request, user)
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])
                
                # Redireccion de Usuarios 
                if user.username == 'csanchez':
                    return redirect('ceo_global')
                elif user.role.alias_rol == "agente_logistico":
                    return redirect('cporte:porte_factura_create')                
                elif user.role.alias_rol == 'ceo':                    
                    return redirect('analytics:empleadossingafete_dashboard')
                elif user.role.alias_rol == 'jefe_grupo' or user.role.alias_rol == 'guardia' or user.role.alias_rol == 'coordinador' or  user.role.alias_rol =='chofer':                    
                    messages.error(request, 'Solo tiene acceso mediante la aplicación móvil si tiene cuenta activa.')
                    return redirect('login')   
                else:                    
                    return redirect('administrador:admin_home')
            else:
                # En caso que no cumpla la autenticación                
                return redirect('login')
        else:
            return redirect('login')
    
    def get(self, request, *args, **kwargs):
        print("ok brother")
        print(self)
        if self.request.user.is_authenticated:
            return redirect('{}'.format(self.request.GET.get('next', 'inicio'))) 

        return super(CustomLoginView, self).get(request, *args, **kwargs)
    
class LoginCustom(LoginView):
    print("Entre")

def login(request): # en desuso
    redirect_to = kwargs.get('next', settings.LOGIN_REDIRECT_URL )
    css_list = ['basic', 'slick', 'custom']
    js_list = ['js_basic', 'js_slick']    
    if request.user.is_authenticated():
        return redirect(redirect_to)
        
    return render(request, "registration/login.htm", { 'css_list': css_list, 'js_list': js_list } )

def home(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)  
    user = User.objects.get(pk= userdict.get('user_id') )  
    return render(request, 'core/home.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,} )

def layout(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_global']
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') )
    incidentes = Incidente.objects.all()
    incidentes11  = Incidente.objects.all()[0:11]
    plantas    = Planta.objects.all()
    clientes   = Cliente.objects.all()   
    return render(request, 'core/layout.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )

def home_plantas(request):
    css_list = ['basic', 'metismenu', 'slick', 'mapbox', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu']
    plot_div = charts.mapa_plantas() 
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') )
    return render(request, 'core/home_plantas.html', { 'css_list': css_list, 'js_list': js_list, 'plot_div': plot_div, 'userdict': userdict, 'user': user} )
    
def ceo_dashboard(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)  
    user = User.objects.get(pk= userdict.get('user_id') )  
    return render(request, 'core/ceo/dashboard.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,} )

def ceo(request):
    css_list = ['basic', 'slick', 'mapbox', 'custom']
    js_list = ['js_basic', 'js_slick', 'js_charts']
    
    userdict = user_validation.validate(request)   
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/ceo.html', { 'css_list': css_list, 'js_list': js_list, 'user': user} )

#Vista de dashboard general
def informe_total(request):
    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']

    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_clipboard', 'js_fancybox' ]
    
    if request.user.username == "acorp":
        cliente = request.user.cliente
        if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
            plantas = Planta.objects.filter(cliente=cliente)
        else:
            nombreplanta = request.user.planta
            plantas = Planta.objects.filter(nombre=nombreplanta)

        incidentes = Incidente.objects.all()
        #plantas = Planta.objects.all()
        clientes = Cliente.objects.all()
        tipo_incidentes = TipoIncidente.objects.all()
        ciudades = Ciudad.objects.all()

        cliente = request.user.cliente
        plantas_v = Planta.objects.get(nombre=nombreplanta)
        
        plantas = Planta.objects.all()
        return render(request, 'core/informe_total.html', { 'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes,'plantas': plantas, 'clientes': clientes, 'tipo_incidentes': tipo_incidentes, 'ciudades': ciudades, 'vcliente': cliente,'vplantas': plantas_v} )
    else:
        return render(request, 'core/informe_total_mant.html', {'css_list': css_list, 'js_list': js_list})

# Vistas DEMO CEO
def ceo_global(request):
    if request.user.role.alias_rol=='coordinador' or request.user.role.alias_rol=='jefe_grupo' or request.user.role.alias_rol=='guardia' or request.user.role.alias_rol=='chofer':        
        messages.error(request, 'Solo tiene acceso mediante la aplicación móvil si tiene cuenta activa.')
        return redirect('login')
    elif request.user.role.alias_rol == 'VISITANTES':
        return redirect('/analytics/previsitantes')
        
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home']
    #js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_global', 'js_moment']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_mapa_calor', 'js_moment']
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes = Incidente.objects.all()
    incidentes11  = Incidente.objects.all()[0:11]
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente=cliente)
    clientes   = Cliente.objects.all()    
    
    return render(request, 'core/ceo_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11, 'cliente': cliente } )

def ceo_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/ceo_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def ceo_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    plot_div = charts.chart_rutas_ceo_master() 
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/ceo_master.html', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def ceo_master_modulo_general(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_master_modulo_general']    
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes = Incidente.objects.all()
    incidentes11  = Incidente.objects.all()[0:11]
    plantas    = Planta.objects.all()
    clientes   = Cliente.objects.all()
    tipo_incidentes = TipoIncidente.objects.all()  

    estadosfuerza = EstadoFuerza.objects.filter(planta_id=user.planta_id).order_by("-fecha_inicio")
    return render(request, 'core/ceo_master_modulo_general.html', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11, 'tipo_incidentes': tipo_incidentes, 'recomendaciones':r, 'estadosfuerza': estadosfuerza } )

def ceo_master_yz_benito_juarez(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_master_planta']
    pBenitoJuarezObj = Planta.objects.filter(alias='benitojuarez').first()  
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/ceo_master_yz_benito_juarez.html', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'pBenitoJuarezObj': pBenitoJuarezObj} )

def ceo_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)   
    user = User.objects.get(pk= userdict.get('user_id') )  
    return render(request, 'core/ceo_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

# Vistas DEMO VICEPRESIDENTE
def vice_global(request):
    css_list    = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list     = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_global']
    
    userdict     = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes   = Incidente.objects.all()
    incidentes11 = Incidente.objects.all()[0: 11]
    plantas      = Planta.objects.all()
    clientes     = Cliente.objects.all() 

    return render(request, 'core/vice_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )

def vice_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vice_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def vice_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)  
    user = User.objects.get(pk= userdict.get('user_id') )   
    return render(request, 'core/vice_master.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def vice_master_modulo_general(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_master_modulo_general']    
    
    userdict     = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes   = Incidente.objects.all()
    incidentes11 = Incidente.objects.all()[0: 11]
    plantas      = Planta.objects.all()
    clientes     = Cliente.objects.all()
    return render(request, 'core/vice_master_modulo_general.html', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )

def vice_master_yz_benito_juarez(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_master_planta']
    pBenitoJuarezObj = Planta.objects.filter(alias='benitojuarez').first()  
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vice_master_yz_benito_juarez.html', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'pBenitoJuarezObj': pBenitoJuarezObj} )

def vice_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request) 
    user = User.objects.get(pk= userdict.get('user_id') )    
    return render(request, 'core/vice_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

# Vistas DEMO VICEPRESIDENTE LA
def vicela_global(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vicela_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def vicela_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vicela_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def vicela_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vicela_master.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def vicela_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/vicela_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

# Vistas DEMO GERENTE REGIONAL
def gtereg_global(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gtereg_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gtereg_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gtereg_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gtereg_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gtereg_master.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gtereg_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gtereg_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

# Vistas DEMO GERENTE DE PLANTA
def gteplanta_global(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request) 
    user = User.objects.get(pk= userdict.get('user_id') )    
    return render(request, 'core/gteplanta_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplanta_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplanta_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplanta_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplanta_master.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplanta_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplanta_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

# Vistas DEMO GERENTE DE PLANTAS PLUS
def gteplus_global(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplus_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplus_pais(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)  
    user = User.objects.get(pk= userdict.get('user_id') )   
    return render(request, 'core/gteplus_pais.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplus_master(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplus_master.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def gteplus_detalle(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home']
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/gteplus_detalles.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def swidgets_plotly_histograma(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic']
    plot_div = charts.chart_histograma() 
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_histograma.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} ) 

def swidgets_plotly_barchart_grupo_vertical(request):  
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']  
    plot_div = charts.chart_barchart_grupo_vertical()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_grupo_vertical.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_grupo_horizontal(request):   
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar'] 
    plot_div = charts.chart_barchart_grupo_horizontal()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_grupo_horizontal.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_grupo_horizontal_lbls_inclinadas(request): 
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']   
    plot_div = charts.chart_barchart_grupo_horizontal_lbls_inclinadas()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_grupo_horizontal_lbls_inclinadas.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_simple_vertical(request):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']     
    plot_div = charts.chart_barchart_simple_vertical()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_simple_vertical.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

def swidgets_plotly_barchart_simple_vertical_etiquetas_fijas(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    plot_div = charts.chart_barchart_simple_vertical_etiquetas_fijas()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_simple_vertical_etiquetas_fijas.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_color_individual(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    plot_div = charts.chart_barchart_color_individual()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_color_individual.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_ancho_individual(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    plot_div = charts.chart_barchart_ancho_individual()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_ancho_individual.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def swidgets_plotly_barchart_estilizada(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    plot_div = charts.chart_barchart_estilizada()
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/plotly_barchart_estilizada.htm', context={'plot_div': plot_div, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user})

def dashdemo22(request):    
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic']
    dash_div = dash.dashapp() 
    
    userdict = user_validation.validate(request)    
    user = User.objects.get(pk= userdict.get('user_id') ) 
    return render(request, 'core/swidgets/graficas/dashdemo.htm', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user} )

class GeneratePDF3(View):
        
    def get(self, request, *args, **kwargs):        
        try:            
            qr = request.GET.get('qr')                        
            
        except KeyError:
            qr = "nada"           
        
        qr = qr.replace(" ", "%20")        
        main_data = { 
            'data': "https://chart.apis.google.com/chart?cht=qr&chs=230x230&chl=" + qr,
            'nombre':'Garita',
            'idrondin': '1'
        }
        pdf = render_to_pdf('core/pdf/qrcodes.html', main_data)        
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "codigo_qr_puntos_de_rondin.pdf"
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:   
            content = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")

def mapa_calor(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_global', 'js_moment']
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes = Incidente.objects.all()
    incidentes11  = Incidente.objects.all()[0:11]
    plantas    = Planta.objects.all()
    clientes   = Cliente.objects.all()
    
    return render(request, 'core/mapa_calor.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )
            
def progreso_incidentes(request):    
    
   # try:
        
        #go = list(Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')).filter(fecha='2019-12-24') )
    print('hi')
    total_incidentes = Incidente.objects.count()
    incidentes = list( Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')) )
    #incidentes = json.loads(serializers.serialize("json",incidentes))
    obj_incidentes = {
        "Res": 'OK',
        "Total_Incidentes": total_incidentes,
        "Incidente": incidentes
    }

    return JsonResponse(obj_incidentes, safe=False)

def parseRSS( rss_url ):
    return feedparser.parse( rss_url )



def getHeadlines(rss_url):
    headlines = []
    to_json = dict()
    json_object = []
    print(rss_url)
    feed = parseRSS(rss_url)
    
    for newsitem in feed['items']:

        """
        to_json += (
            ("title", newsitem['title']),
            ("link", newsitem['link']),
            ("description", newsitem['description']), 
            
        )
        
        #print(to_json)
        
        to_json += { 
            "title": newsitem['title'], 
            "link": newsitem['link'],
            "description": newsitem['description']
        }
        """

        to_json.update(
            {
                "noticia": {
                    "title": newsitem['title'],
                    "link": newsitem['link'],
                    "description": newsitem['description']
                }
            }
        )
        #print(to_json)
        #json_object += json.loads(to_json)
        #headlines.append(newsitem['title'])
        #headlines.append(newsitem['link'])
        #headlines.append(newsitem['description'])
        #headlines.append(newsitem['source'])
        #headlines.append(newsitem['source'].url)

    
    return to_json
    #return headlines
    #return list(to_json)
    #return JsonResponse(list(to_json), safe=False)

def news_rss(request):    
    criterio = request.GET.get('criterio')    
    
    if criterio != None:
        urlnews = "https://news.google.com/rss/search?q="+str(criterio)+"&hl=es-419&gl=MX&ceid=MX:es-419"
    else:
        urlnews = "https://news.google.com/rss?hl=es-419&gl=MX&ceid=MX:es-419&limit=10"
    
    headlines = []
    to_json = dict()
    json_object = []
    
    feed = parseRSS(urlnews)
    
    return JsonResponse(feed, safe=False)
    
