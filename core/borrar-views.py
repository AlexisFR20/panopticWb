from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse
from . import charts
from . import dash
from django.utils.html import escape
from django.utils import timezone
from . import user_validation
from entorno.models import Incidente
from core.models import Planta, Cliente, User
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import View
from core.utils import render_to_pdf
from django.template.loader import get_template
import datetime

def error_404_view(request, exception):    
    return render(request, 'core/errores/404.html')

def error_404_view_dev(request):    
    return render(request, 'core/errores/404.html') 

class CustomLoginView(LoginView):
    """
    Custom login view.
    """
    def post(self, request, *args, **kwargs):            
        username = request.POST.get('username')
        password = request.POST.get('password')        
        
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
                elif user.role.alias_rol == 'ceo':                    
                    return redirect('analytics:empleadossingafete_dashboard')
                elif user.role.alias_rol == 'jefe_grupo':                    
                    return redirect('administrador:admin_rondines_resumen')
                elif user.role.alias_rol == 'guardia':                    
                    #return redirect('guardia_home')                
                    return redirect('administrador:admin_rondines_resumen')
                else:                    
                    return redirect('administrador:admin_home')
            else:
                # En caso que no cumpla la autenticación                
                return redirect('login')
        else:
            return redirect('login')
    
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('{}'.format(self.request.GET.get('next', 'ceo_global')))

        return super(CustomLoginView, self).get(request, *args, **kwargs)
    
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
# Vistas DEMO CEO
def ceo_global(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_global']
    
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') ) 
    incidentes = Incidente.objects.all()
    incidentes11  = Incidente.objects.all()[0:11]
    plantas    = Planta.objects.all()
    clientes   = Cliente.objects.all()
    
    return render(request, 'core/ceo_global.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )

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
    return render(request, 'core/ceo_master_modulo_general.html', context={'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11 } )

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