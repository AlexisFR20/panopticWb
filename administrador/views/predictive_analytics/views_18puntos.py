from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from analytics.models import EvidenciaPunto, F_18_puntos_Trailer 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from core import user_validation
from django.http import HttpResponseRedirect, JsonResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.sites.models import Site  
from arnes.models import Papeleta

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']

# 18 Puntos - Historial
def admin_18puntos_historial(request):
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()    
    revisiones = F_18_puntos_Trailer.objects.all().order_by('-fecha')  
    
    return render(request, 'administrador/predictive/18puntos-historial.html', {'css_list': css_list, 'js_list': js_list, 'clientes': clientes, 'plantas': plantas, 'revisiones': revisiones})
    
def admin_18puntos_historial_show(request, rev_id):
    revision18 = F_18_puntos_Trailer.objects.get(pk=rev_id)        
  
    return render(request, 'administrador/predictive/18puntos-historial-show.html', { 'css_list': css_list, 'js_list': js_list, 'revision': revision18 })

# Generación de reporte via AJAX de 18 Puntos 
def ajax_load_reporte_18puntos(request):
    cliente_id = request.GET.get('cliente_id')   
    planta_id = request.GET.get('planta_id')   
    fec_inicio = request.GET.get('fec_inicio')   
    fec_fin = request.GET.get('fec_fin')    
    
    if cliente_id == "0"  and planta_id == "0":   # Solo fechas ingresadas     
        revisiones = F_18_puntos_Trailer.objects.filter(fecha__gte=fec_inicio, fecha__lte=fec_fin).order_by('fecha')          
    
    elif cliente_id == "0" and planta_id != "0":  #Unidad de negocio y fechas        
        revisiones = F_18_puntos_Trailer.objects.filter(planta_id=planta_id, fecha__gte=fec_inicio, fecha__lte=fec_fin).order_by('fecha')     

    elif cliente_id != "0" and planta_id == "0":  #Cliente y fechas ingresadas        
        revisiones = F_18_puntos_Trailer.objects.filter(planta__cliente_id=cliente_id, fecha__gte=fec_inicio, fecha__lte=fec_fin).order_by('fecha')
        
    elif cliente_id != "0" and planta_id != "0":  #Con todos los parámetros        
        revisiones = F_18_puntos_Trailer.objects.filter(planta_id=planta_id, fecha__gte=fec_inicio, fecha__lte=fec_fin).order_by('fecha')         
        
    return render(request, 'administrador/options/rep_18puntos.html', {'revisiones': revisiones })

# 18 Puntos - Reportes
def admin_18puntos_reportes(request):       
    revisiones = F_18_puntos_Trailer.objects.all().order_by('fecha')  
    
    return render(request, 'administrador/predictive/18puntos-reportes.html', { 'css_list': css_list, 'js_list': js_list, 'clientes': clientes, 'plantas': plantas, 'revisiones': revisiones })