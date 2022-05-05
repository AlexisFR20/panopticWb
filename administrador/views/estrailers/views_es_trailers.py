from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from API.serializers import RondinSerializer
from entorno.models import Incidente
from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_18_puntos_Trailer, F_ES_Trailers
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

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]
# Obtenciión de lista mínima de usuarios de tipo cliente y de Águilas
ultimos_usuarios_aguilas  = User.objects.filter(groups__name='aguilas', is_active=1)[:5]
ultimos_usuarios_clientes = User.objects.filter(groups__name='cliente', is_active=1)[:5]
all_aguilas_users  = User.objects.filter(groups__name='aguilas', is_active=1)

# 18 Puntos - Historial
def admin_es_trailers_historial(request):
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id'))    
    estrailers = F_ES_Trailers.objects.all()    
    
    return render(request, 'administrador/estrailers/historial.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user,  'estrailers': estrailers })

# 18 Puntos - Ver
def admin_es_trailers_ver(request, estra_id):
	
	estrailer = F_ES_Trailers.objects.get(pk=estra_id)

	return render(request, 'administrador/estrailers/ver.html', { 'css_list': css_list, 'js_list': js_list, 'estrailer': estrailer })