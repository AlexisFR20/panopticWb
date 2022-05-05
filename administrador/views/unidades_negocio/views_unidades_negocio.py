from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role, Region
from core.utils import permiso
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

#Vista con funcionalidad para AJAX
def ajax_load_cinterno(request):
    user_id = request.GET.get('user_id')    
    cinterno = User.objects.get(pk=user_id)    
    return render(request, 'administrador/options/cinternos_dropdown_options.html', {'cinterno': cinterno})

# Vistas de Unidades de Negocio en Dashboard de Administrador
def admin_un_index(request):       
    
    roles = ['ceo', 'vicepresidente', 'vicepresidente_la', 'gerente_regional', 'gerente_planta', 'seguridad_interna', 'administrador', 'gerente_operativo']
    
    roleUsuario = request.user.role.alias_rol
    
    acceso = permiso(roles, roleUsuario)  
    
    plantas = None
    
    if roleUsuario == 'gerente_planta' or roleUsuario == 'seguridad_interna'  or roleUsuario == 'gerente_operativo':
        #Solo regresa su planta respectiva
        plantas = request.user.planta
    else:
        plantas = Planta.objects.all()
    
    return render(request, 'administrador/unidades_negocio/index.html', { 'css_list': css_list, 'js_list': js_list,  'plantas': plantas, 'plantas_relevantes': plantas_relevantes, 'acceso': acceso })
  
def admin_un_edit(request, un_id):             
    planta = Planta.objects.get(pk= un_id )   # Unidad - Planta en  edición
    clientes = Cliente.objects.all()
    regiones = Region.objects.all()
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar',  'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_unidad_negocio_actualizar' ] 
    #Para obtener los contactos internos válidos para la unidad de negocio
    # 1. Que tenga el cliente de la unidad de negocio: planta.client_id == user.client_id
    # 2.  Agregar más criterios (opcionales)
    cinternos = User.objects.filter(planta=planta)       
    
    try:
        cinterno_sel = User.objects.get(pk= planta.cinterno_id )        
        #cinterno_sel = get_object_or_404(User, pk=planta.cinterno_id)
    except:        
        cinterno_sel = None    
        
    # SI la forma fue enviada, se procesan los datos            
    if request.method == 'POST':
        if request.POST.get('nombre'):
            planta.nombre = request.POST['nombre']
            
        if request.POST.get('alias'):
            planta.alias = request.POST['alias']
            
        if request.POST.get('direccion'):
            planta.direccion = request.POST['direccion']
            
        if request.POST.get('ciudad'):
            planta.ciudad = request.POST['ciudad'] 
            
        if request.POST.get('estado'):
            planta.estado = request.POST['estado']
            
        if request.POST.get('pais'):
            planta.pais = request.POST['pais']
            
        # Establece el valor de Cliente si éste ha sido modificado / asignado
        if request.POST.get('cliente') == "0":
            planta.cliente_id = None 
        else:
            planta.cliente_id = request.POST.get('cliente') 
            
        # Establece el Contacto Interno asociado mismo que es de tipo USER
        if request.POST.get('cinterno') == "0":
            planta.cinterno_id = None 
        else:
            planta.cinterno_id = request.POST.get('cinterno')  
        
        if request.POST.get('lat'):
            planta.lat = request.POST['lat']
            
        if request.POST.get('lng'):
            planta.lng = request.POST['lng']
            
        if request.POST.get('region'):
            region_id = int(request.POST['region'])
            planta.region = Region.objects.get(pk=region_id)
            
        if request.POST.get('pais'):
            planta.pais = request.POST['pais']
            
        if(request.POST.get('giro')):
            planta.giro = request.POST['giro'] 
            
        if(request.POST.get('tipo')):
            planta.tipo = request.POST['tipo'] 
            
        #Criterios de Evaluación
        if(request.POST.get('estatus_cobertura_estable')):
            planta.estatus_cobertura_estable = request.POST['estatus_cobertura_estable'] 
            
        if(request.POST.get('estatus_cobertura_relevante')):
            planta.estatus_cobertura_relevante = request.POST['estatus_cobertura_relevante'] 
            
        if(request.POST.get('estatus_ausentismo_estable')):
            planta.estatus_ausentismo_estable = request.POST['estatus_ausentismo_estable'] 
        
        if(request.POST.get('estatus_ausentismo_relevante')):
            planta.estatus_ausentismo_relevante = request.POST['estatus_ausentismo_relevante'] 
            
        if(request.POST.get('estatus_rotacion_estable')):
            planta.estatus_rotacion_estable = request.POST['estatus_rotacion_estable'] 
            
        if(request.POST.get('estatus_rotacion_relevante')):
            planta.estatus_rotacion_relevante = request.POST['estatus_rotacion_relevante']                       
            
        if(request.POST.get('mails_zona')):
            planta.mails_zona = request.POST['mails_zona'] 
        
        if(request.POST.get('mails_analisis_riesgo')):
            planta.mails_analisis_riesgo = request.POST['mails_analisis_riesgo'] 
            
        if(request.POST.get('mails_dd')):
            planta.mails_dd = request.POST['mails_dd'] 
            
        if(request.POST.get('mails_predictive')):
            planta.mails_predictive = request.POST['mails_predictive']             

        # Almacenamiento del archivo de imagen, en el caso de haberse agregado
        foto = request.FILES.get('foto', False)     
        if foto:
            
            if settings.DEBUG:
                fs = FileSystemStorage(location='media/avatars/')                
            else:
                fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
            
            fs = FileSystemStorage(location='/home/ubuntu/pgit/media/avatars/')                        
            filename = fs.save(foto.name, foto)            
            planta.foto = 'avatars/' + filename                     
            
        # Registro de cambios en los datos del usuario    
        try:   
            go = planta.save()
            messages.add_message(request,  messages.SUCCESS, 'Unidad de Negocio modificada exitosamente')
        except User.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifcó la Unidad de Negocio, hubo un error.')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_un_edit', un_id=un_id)   
    
    return render(request, 'administrador/unidades_negocio/edit.html', { 'css_list': css_list, 'js_list': js_list,  'planta': planta, 'clientes': clientes, 'cinternos': cinternos, 'cinterno_sel': cinterno_sel, 'regiones': regiones  }) 

def admin_un_delete(request, un_id):
    try:
        go = Planta.objects.filter(id=un_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Unidad de negocio borrada exitosamente')
    except Planta.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró la unidad de negocio, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_un_index')

def admin_sucursales_index(request):     
    user = User.objects.get(pk= userdict.get('user_id') )        
    
    return render(request, 'administrador/sucursales/index.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'plantas_relevantes': plantas_relevantes })