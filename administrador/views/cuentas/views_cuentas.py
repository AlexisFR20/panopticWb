from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.forms.models import model_to_dict
from core.models import Role, Permisos, Permrol, Areapermiso
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json
from django.core.cache import cache
from core.utils import *
#from ddmanagement.forms import CajaForm
#from ddmanagement.models import Caja 

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]        
    
def CuentasPrincipal(request):
    # SI la forma fue enviada, se procesan los datos
    if request.method == 'POST':        
        user = request.user               
        getPassContent = request.POST['password']                
        # Si hay nueva contraseña se modifica
        if getPassContent:
            user.set_password(getPassContent)      
            
            # Registro de cambios en los datos del usuario    
            try:   
                go = user.save()
                messages.add_message(request,  messages.SUCCESS, 'Contaseña modificada exitosamente')
            except User.DoesNotExist:
                go = None        
                messages.add_message(request,  messages.ERROR, 'No se modifico la contraseña, hubo un error.')    
      
    return render(request, 'administrador/cuentas/principal.html', { 'css_list': css_list, 'js_list': js_list })

def CuentasPermisosPorTipo(request):  
    areas = Areapermiso.objects.all().order_by('orden')
    roles = Role.objects.all().order_by('grupo')
    permisos = Permisos.objects.all()
    permroles = Permrol.objects.all()
              
    return render(request, 'administrador/cuentas/permisos_bytype.html', { 'css_list': css_list, 'js_list': js_list, 'areas': areas, 'roles': roles, 'permisos': permisos, 'permroles': permroles }) 
