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

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]
# Obtenciión de lista mínima de usuarios de tipo cliente y de Águilas
ultimos_usuarios_aguilas  = User.objects.filter(groups__name='aguilas', is_active=1)[:5]
ultimos_usuarios_clientes = User.objects.filter(groups__name='cliente', is_active=1)[:5]
all_aguilas_users  = User.objects.filter(groups__name='aguilas', is_active=1)
clientes = User.objects.filter(groups__name='cliente')

def admin_perfiles_clientes_index(request):
    userdict = user_validation.validate(request)
    user = User.objects.get(pk= userdict.get('user_id') )    
        
    return render(request, 'administrador/perfiles_clientes/index.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user': user, 'clientes': clientes })

def admin_perfiles_cliente_show(request, user_id):
    userdict = user_validation.validate(request)    
    userToShow = User.objects.get(pk= user_id )
    groups = Group.objects.all()
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()
    roles = Role.objects.all()        
  
    return render(request, 'administrador/perfiles_clientes/show.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'userToShow': userToShow, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })

def admin_perfiles_cliente_edit(request, user_id):
    userdict = user_validation.validate(request)    
    user_in_edition = User.objects.get(pk= user_id )
    groups = Group.objects.all()
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()
    roles = Role.objects.all()    
    
    # SI la forma fue enviada, se procesan los datos
    if request.method == 'POST':
        
        user_in_edition.username = request.POST['username']
        user_in_edition.first_name = request.POST['first_name']
        user_in_edition.last_name = request.POST['last_name']
        user_in_edition.email = request.POST['email']       
        user_in_edition.is_staff = request.POST['is_staff']
        user_in_edition.is_active = request.POST['is_active']
        # user_in_edition.password = request.POST['password'] 
        
        getPassContent = request.POST['password']        
        # Si hay nueva contraseña se modifica
        if getPassContent:                        
            user_in_edition.set_password(getPassContent)        
      
        user_in_edition.grupos = request.POST.getlist('grupos')                
        
        #Obtiene lla lista de los valores en el SELECT MÚLTIPLE de Grupos
        lista_grupos = request.POST.getlist('grupos')        
        user_in_edition.groups.clear()
        
        for gp  in lista_grupos:
            group = Group.objects.get(name=gp)
            user_in_edition.groups.add(group)            
        
        # Establece el valor de Cliente si éste ha sido modificado / asignado
        if request.POST.get('cliente') == "0":
            user_in_edition.cliente_id = None 
        else:
            user_in_edition.cliente_id = request.POST.get('cliente') 
         
        # Establece el valor la Unidad de Negocio si ésta ha sido modificada / asignada
        if request.POST.get('planta') == "0":
            user_in_edition.planta_id = None 
        else:
            user_in_edition.planta_id = request.POST.get('planta') 
        
        # Establece el valor de; Rol del Usuario  si éste ha sido modificado / asignado
        if request.POST.get('role') == "0":
            user_in_edition.role_id = None 
        else:
            user_in_edition.role_id = request.POST.get('role')         
        
        # Almacenamiento del archivo de imagen, en el caso de haberse agregado
        imagen = request.FILES.get('imagen', False)     
        if imagen:
            fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')  
            filename = fs.save(imagen.name, imagen)            
            user_in_edition.imagen = 'avatars/' + imagen.name            
        
        # Registro de cambios en los datos del usuario    
        try:   
            go = user_in_edition.save()
            messages.add_message(request,  messages.SUCCESS, 'Cliente modificado exitosamente')
        except User.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifcó el cliente, hubo un error.')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_perfiles_cliente_edit', user_id=user_in_edition.id)                 
    
    return render(request, 'administrador/perfiles_clientes/edit.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user_in_edition': user_in_edition, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })

def admin_perfiles_cliente_create(request):
    userdict = user_validation.validate(request)        
    groups = Group.objects.all()
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()
    roles = Role.objects.all()    
    
    # SI la forma fue enviada, se procesan los datos
    if request.method == 'POST':
        
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']       
        is_staff = request.POST['is_staff']
        is_active = request.POST['is_active']
        date_joined = request.POST['date_joined_real']              
        
        getPassContent = request.POST['password']              
        
        try:   
            user_in_edition = User.objects.create_user(
                username = username,
                first_name = first_name,
                last_name = last_name,                
                email = email,
                is_staff = is_staff,
                is_active = is_active,
                date_joined = date_joined
            )
            user_in_edition.save( )
            
            # Almacenamiento del archivo de imagen, en el caso de haberse agregado           
            
            imagen = request.FILES.get('imagen', False)     
            if imagen:
                if settings.DEBUG:
                    fs = FileSystemStorage(location='media/avatars/')                
                else:
                    fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
                
                fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
                filename = fs.save(imagen.name, imagen)            
                user_in_edition.imagen = 'avatars/' + filename    
            
            # Si hay nueva contraseña se modifica
            if getPassContent:                            
                user_in_edition.set_password(getPassContent)        
        
            grupos = request.POST.getlist('grupos')                
            
            #Obtiene lla lista de los valores en el SELECT MÚLTIPLE de Grupos
            lista_grupos = request.POST.getlist('grupos')        
            user_in_edition.groups.clear()
            
            for gp  in lista_grupos:
                group = Group.objects.get(name=gp)
                user_in_edition.groups.add(group)            
            
            # Establece el valor de Cliente si éste ha sido modificado / asignado
            if request.POST.get('cliente') == "0":
                user_in_edition.cliente_id = None 
            else:
                user_in_edition.cliente_id = request.POST.get('cliente') 
            
            # Establece el valor la Unidad de Negocio si ésta ha sido modificada / asignada
            if request.POST.get('planta') == "0":
                user_in_edition.planta_id = None 
            else:
                user_in_edition.planta_id = request.POST.get('planta') 
            
            # Establece el valor de; Rol del Usuario  si éste ha sido modificado / asignado
            if request.POST.get('role') == "0":
                user_in_edition.role_id = None 
            else:
                user_in_edition.role_id = request.POST.get('role')  
            
            user_in_edition.save( )
            messages.add_message(request,  messages.SUCCESS, 'Cliente creado exitosamente')
            
            return redirect('administrador:admin_perfiles_cliente_edit', user_id=user_in_edition.id)
        except User.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se creo el perfil del cliente, hubo un error.')
            return render(request, 'administrador/perfiles_clientes/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })                          
    
    return render(request, 'administrador/perfiles_clientes/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })                      

def admin_perfiles_cliente_delete(request, user_id):
    try:
        go = User.objects.filter(id=user_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Cliente borrado exitosamente')
    except User.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró el cliente, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_perfiles_clientes_index')