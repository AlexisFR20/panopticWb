from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from ddmanagement.models import Movimiento, gpsdevice
from django.core.cache import cache

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_gps_all']

def dashboard_dd(request):                
    #Verifica que esté definido vcliene 
    cliente = request.user.cliente    
    if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
        plantas = Planta.objects.filter(cliente=cliente)
    else:
        nombreplanta = request.user.planta       
        plantas = Planta.objects.filter(nombre=nombreplanta)
        
    vmovimientos = Movimiento.objects.filter()
    gpsdevices = gpsdevice.objects.all()
        
    return render(request, 'administrador/ddmanagement/dashboard/dashboard.html', { 'css_list': css_list, 'js_list': js_list, 'vcliente': cliente, 'vplantas': plantas, 'gpsdevices': gpsdevices }) 