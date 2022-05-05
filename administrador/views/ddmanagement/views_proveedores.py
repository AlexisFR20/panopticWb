from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from analytics.models import F_Visitantes
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
css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_fancybox' ]

# Vistas de movimientos en Dashboard de Administrador
def admin_proveedores_index(request): 
    proveedores = F_Visitantes.objects.filter(tipo='proveedor')  
    
    return render(request, 'administrador/ddmanagement/proveedores/index.html', { 'css_list': css_list, 'js_list': js_list, 'proveedores': proveedores })

def admin_proveedores_create(request):
    
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de crear del proveedor 
        if request.POST.get('empresa'):
            empresa = request.POST['empresa']

        if request.POST.get('nombre'):
            nombre = request.POST['nombre']

        if request.POST.get('email'):
            email = request.POST['email']

        if request.POST.get('telefono'):
            telefono = request.POST['telefono']
        
        if request.POST.get('domicilio'):
            domicilio = request.POST['domicilio']       

         # Registro de cambios en los datos del proveedor    
        try:   
            proveedor = F_Visitantes.objects.create(
                empresa = empresa,
                nombre = nombre,
                email = email,                
                telefono = telefono,
                domicilio = domicilio,
                tipo='proveedor',
                confirmo_anfitrion=False
            )
            proveedor.save()

            # Almacenamiento del archivo de imagen, en el caso de haberse agregado
            foto = request.FILES.get('foto', False)     
            if foto:                
                if settings.DEBUG:
                    fs = FileSystemStorage(location='media/avatars/')                
                else:
                    fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
                
                #fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
                filename = fs.save(foto.name, foto)                
                proveedor.foto = 'avatars/' + filename
                proveedor.save()

            messages.add_message(request, messages.SUCCESS, 'Proveedor creado exitosamente')
            return redirect('administrador:admin_proveedores_index')      
        except F_Visitantes.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el Proveedor, hubo un error.')
            
        return redirect('administrador:admin_proveedores_index')     
    
    return render(request, 'administrador/ddmanagement/proveedores/create.html', { 'css_list': css_list, 'js_list': js_list })

def admin_proveedores_edit(request, prov_id):
    
    try:
        proveedor = F_Visitantes.objects.get(pk=prov_id)
    except:        
        proveedor = None

    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del proveedor 
        if request.POST.get('empresa'):
            proveedor.empresa = request.POST['empresa']

        if request.POST.get('nombre'):
            proveedor.nombre = request.POST['nombre']

        if request.POST.get('email'):
            proveedor.email = request.POST['email']

        if request.POST.get('telefono'):
            proveedor.telefono = request.POST['telefono']
        
        if request.POST.get('domicilio'):
            proveedor.domicilio = request.POST['domicilio']

        # Almacenamiento del archivo de imagen, en el caso de haberse agregado
        foto = request.FILES.get('foto', False)     
        if foto:
            
            if settings.DEBUG:
                fs = FileSystemStorage(location='media/avatars/')                
            else:
                fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
            
            #fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
            filename = fs.save(foto.name, foto)            
            proveedor.foto = 'avatars/' + filename   

         # Registro de cambios en los datos del proveedor    
        try:   
            go = proveedor.save()            
            messages.add_message(request,  messages.SUCCESS, 'Proveedor modificado exitosamente')
        except F_Visitantes.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el registro del proveedor, hubo un error.')
            
        return redirect('administrador:admin_proveedores_edit', prov_id=prov_id)          
    
    return render(request, 'administrador/ddmanagement/proveedores/edit.html', { 'css_list': css_list, 'js_list': js_list, 'proveedor': proveedor })

def admin_proveedores_delete(request, prov_id):
    try:
        go = F_Visitantes.objects.filter(id=prov_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Proveedor borrado exitosamente')
    except F_Visitantes.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró al proveedor, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_proveedores_index')