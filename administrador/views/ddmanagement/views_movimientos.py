from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from core import user_validation
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

#Este archivo es el bueno Ahora mismo

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

# Obtenciión de lista mínima de usuarios de tipo cliente y de Águilas
ultimos_usuarios_aguilas  = User.objects.filter(groups__name='aguilas', is_active=1)[:5]
ultimos_usuarios_clientes = User.objects.filter(groups__name='cliente', is_active=1)[:5]
all_aguilas_users  = User.objects.filter(groups__name='aguilas', is_active=1)
all_clientes_users = User.objects.filter(groups__name='cliente')

# Vistas de movimientos en Dashboard de Administrador
def admin_mapa_movimientos(request):     
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker']
    
    return render(request, 'administrador/ddmanagement/movimientos/mapa.html', { 'css_list': css_list, 'js_list': js_list })
    
def mapa_movimientos(request):     #Versión mejorada
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker']
    
    return render(request, 'administrador/ddmanagement/movimientos/mapa_movimientos.html', { 'css_list': css_list, 'js_list': js_list })

# Vistas de movimientos en Dashboard de Administrador
def admin_movimiento_listado(request): 
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id') )
    all_users   = User.objects.all()
    #l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    #l_as_list = list(l)       
    return render(request, 'administrador/ddmanagement/movimientos/index.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'all_users': all_users })

def admin_movimiento_create(request): 
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id') )
    all_users   = User.objects.all()
    #l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    #l_as_list = list(l)       
    return render(request, 'administrador/ddmanagement/movimientos/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'all_users': all_users })

def admin_movimiento_edit(request, mov_id): 
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id') )
    all_users   = User.objects.all()
    #l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    #l_as_list = list(l)       
    return render(request, 'administrador/ddmanagement/movimientos/edit.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'all_users': all_users })

