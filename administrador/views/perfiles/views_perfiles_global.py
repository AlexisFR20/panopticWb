from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role, Notificacion, PorteCliente
from core import user_validation
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings

n = Notificacion.objects.filter(visto = False)

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

# Vistas de Perfiles en Dashboard de Administrador
def admin_perfiles_global_index(request): 
    userdict    = user_validation.validate(request)
    user          = User.objects.get(pk= userdict.get('user_id') )
    all_users   = User.objects.all().order_by('id')
    #l = request.user.groups.values_list('name',flat = True) # QuerySet Object
    #l_as_list = list(l)       
    return render(request, 'administrador/perfiles_global/index.html', { 'css_list': css_list, 'js_list': js_list, 'notificaciones': n, 'userdict': userdict, 'user': user,  'all_users': all_users })

def admin_perfiles_global_show(request, user_id):
    userdict = user_validation.validate(request)    
    userToShow = User.objects.get(pk= user_id )
    groups = Group.objects.all()
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()
    roles = Role.objects.all()        
  
    return render(request, 'administrador/perfiles_global/show.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'userToShow': userToShow, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })

def admin_perfiles_global_edit(request, user_id):
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
            
        if request.POST.get('tel_pral'):
            user_in_edition.tel_pral = request.POST['tel_pral']
            
        if request.POST.get('tel_alt'):
            user_in_edition.tel_pral = request.POST['tel_alt']            
        
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
            
        
        # Registro de cambios en los datos del usuario    
        try:   
            go = user_in_edition.save()
            messages.add_message(request,  messages.SUCCESS, 'Usuario modificado exitosamente')
        except User.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifico el usuario, hubo un error.')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_perfiles_global_edit', user_id=user_in_edition.id)
        # if a GET (or any other method) we'll create a blank form            
    
    return render(request, 'administrador/perfiles_global/edit.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user_in_edition': user_in_edition, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })

def admin_perfiles_global_create(request):
    userdict = user_validation.validate(request)        
    groups = Group.objects.all()
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()
    roles = Role.objects.all()    
    porteClientes = PorteCliente.objects.all()
    
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
                fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')  
                filename = fs.save(imagen.name, imagen)            
                user_in_edition.imagen = 'avatars/' + imagen.name   
            
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

            # Establece valor del cliente de carta porte 
            if request.POST.get('porteCliente') == "0":
                user_in_edition.portecliente_id = None
            else:
                user_in_edition.portecliente_id = request.POST.get("porteCliente")
            
            user_in_edition.save( )
            messages.add_message(request,  messages.SUCCESS, 'Usuario creado exitosamente')
            
            return redirect('administrador:admin_perfiles_global_edit', user_id=user_in_edition.id)        
        except User.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se creo el perfil del usuario, hubo un error.')  
            return render(request, 'administrador/perfiles_global/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles })                    
    
    return render(request, 'administrador/perfiles_global/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'groups': groups, 'clientes': clientes, 'plantas': plantas, 'roles': roles , 'porteClientes': porteClientes})

def admin_perfiles_global_delete(request, user_id):
    try:
        go = User.objects.filter(id=user_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Usuario borrado exitosamente')
    except User.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró el usuario, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_perfiles_global_index')

def admin_perfiles_global_editRRR(request, user_id):
    userdict            = user_validation.validate(request)    
    user_in_edition = User.objects.get(pk= user_id ) 
    
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        
        form =   NameForm(request.POST)
        form2 = Apellido(request.POST)
        # check whether it's valid:
        if form.is_valid() and form2.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form  = NameForm()
        form2 = Apellido()
        
    
    return render(request, 'administrador/perfiles_global/edit.html', { 'form': form, 'form2': form2, 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'user_in_edition': user_in_edition})
