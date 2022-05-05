from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role, Region, Sucursal, Ciudad
from core import user_validation
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']

js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_clipboard', 'js_fancybox' ]
# Obtención de lista mínima de usuarios de tipo cliente y de Águilas
plantas = Planta.objects.all()
plantas_relevantes = Planta.objects.filter(status='relevante' )
all_users = User.objects.all()


def admin_sucursales_index(request):    
    sucursales = Sucursal.objects.all()  
    
    return render(request, 'administrador/sucursales/index.html', { 'css_list': css_list, 'js_list': js_list, 'sucursales':sucursales })

def admin_sucursales_create(request): 
    regiones = Region.objects.all()
    ciudades = Ciudad.objects.all()       
    
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        if request.POST.get('nombre'):
            nombre = request.POST['nombre']

        if request.POST.get('domicilio'):
            domicilio = request.POST['domicilio']

        if request.POST.get('telefono'):
            telefono = request.POST['telefono']
        
        if request.POST.get('ciudad'):
            ciudad = request.POST['ciudad']

        if request.POST.get('estado'):
            estado = request.POST['estado']

        if request.POST.get('region'):            
            region = Region.objects.get(pk=request.POST['region'])

         # Registro de cambios en los datos de la sucursak    
        try:   
            sucursal = Sucursal.objects.create(
                nombre = nombre,
                domicilio = domicilio,
                telefono = telefono,                
                ciudad = ciudad,
                estado = estado,
                region = region
            )
            sucursal.save()
            messages.add_message(request,  messages.SUCCESS, 'Sucursal creada exitosamente')
        except Sucursal.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se creó la Sucursal, hubo un error.')

        return redirect('administrador:admin_sucursales_index') 
    
    return render(request, 'administrador/sucursales/crear.html', { 'css_list': css_list, 'js_list': js_list, 'regiones':regiones, 'ciudades': ciudades })

def admin_sucursales_edit(request, suc_id):     
    regiones = Region.objects.all()
    ciudades = Ciudad.objects.all()   

    try:
        sucursal = Sucursal.objects.get(pk=suc_id) 
    except:        
        sucursal = None        
    
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        if request.POST.get('nombre'):
            sucursal.nombre = request.POST['nombre']

        if request.POST.get('domicilio'):
            sucursal.domicilio = request.POST['domicilio']

        if request.POST.get('telefono'):
            sucursal.telefono = request.POST['telefono']
        
        if request.POST.get('ciudad'):
            sucursal.ciudad = request.POST['ciudad']

        if request.POST.get('estado'):
            sucursal.estado = request.POST['estado']

        if request.POST.get('region'):            
            sucursal.region = Region.objects.get(pk=request.POST['region'])

         # Registro de cambios en los datos de la sucursak    
        try:   
            go = sucursal.save()
            messages.add_message(request,  messages.SUCCESS, 'Sucursal modificada exitosamente')
        except Sucursal.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifcó la Sucursal, hubo un error.')

        return redirect('administrador:admin_sucursales_edit', suc_id=suc_id)   
    
    return render(request, 'administrador/sucursales/editar.html', {'css_list': css_list, 'js_list': js_list, 'regiones': regiones, 'ciudades': ciudades, 'sucursal': sucursal})
    
def admin_sucursales_delete(request, suc_id):
    try:
        go = Sucursal.objects.filter(id=suc_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Sucursal borrada exitosamente')
    except Sucursal.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_sucursales_index')

def admin_regiones_index(request):    
    regiones = Region.objects.all()  
    
    return render(request, 'administrador/regiones/index.html', {'css_list': css_list, 'js_list': js_list, 'regiones': regiones})
    
def admin_regiones_create(request):     
    
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        if request.POST.get('nombre'):
            nombre = request.POST['nombre']

        if request.POST.get('alias'):
            alias = request.POST['alias']

        if request.POST.get('idnumerico'):
            idnumerico = request.POST['idnumerico']

         # Registro de cambios en los datos de la sucursak    
        try:   
            region = Region.objects.create(
                nombre = nombre,
                alias = alias,
                idnumerico = idnumerico
            )
            region.save()
            messages.add_message(request,  messages.SUCCESS, 'Región creada exitosamente')
        except Region.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se creó la Región, hubo un error.')

        return redirect('administrador:admin_regiones_index') 
    
    return render(request, 'administrador/regiones/crear.html', {'css_list': css_list, 'js_list': js_list})
    
def admin_regiones_edit(request, reg_id):     

    try:
        region = Region.objects.get(pk=reg_id) 
    except:        
        region = None        
    
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición de la región 
        if request.POST.get('nombre'):
            region.nombre = request.POST['nombre']

        if request.POST.get('alias'):
            region.alias = request.POST['alias']

        if request.POST.get('telefono'):
            region.telefono = request.POST['telefono']

         # Registro de cambios en los datos de la sucursak    
        try:   
            go = region.save()
            messages.add_message(request,  messages.SUCCESS, 'Región modificada exitosamente')
        except Region.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifcó la Región, hubo un error.')

        return redirect('administrador:admin_regiones_edit', reg_id=reg_id)   
    
    return render(request, 'administrador/regiones/editar.html', {'css_list': css_list, 'js_list': js_list, 'region':region})
    
def admin_regiones_delete(request, reg_id):
    try:
        go = Region.objects.filter(id=reg_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Región borrada exitosamente')
    except Region.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró la región, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_regiones_index')