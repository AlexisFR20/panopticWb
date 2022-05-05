from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from API.serializers import RondinSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from entorno.models import Incidente
from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_18_puntos_Trailer
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
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_fancybox' ]

# Agregar funciones de vista aqui de Mapa Interactivo
# Crear Rondin
def admin_rondines_rondin_create(request): 
    userdict = user_validation.validate(request) 
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()    
    guardias = User.objects.filter(role__alias_rol="guardia")
    rondines = Rondin.objects.all().order_by('-id')[:5]
    rondin_id=0    
    
    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'datepicker', 'wickedpicker', 'fancybox', 'taginput']
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables',  'js_taginput', 'js_form_validator', 'js_moment', 'js_datepicker' , 'js_wickedpicker',  'js_rondin_create', 'js_mapa_interactivo',  'js_fancybox' ]     
    
    # SI la forma fue enviada, se procesan los datos            
    if request.method == 'POST':
        if request.POST.get('nombre'):
            nombre = request.POST['nombre']
            
        if request.POST.get('admin_aguilas'):
            aguilas_id = int(request.POST['admin_aguilas'])
            if aguilas_id > 0:
                admin_aguilas = User.objects.get(pk=aguilas_id) 
            
        if request.POST.get('cliente'):
            cliente_id = int(request.POST['cliente'])
            if  cliente_id> 0:
                cliente = Cliente.objects.get(pk=cliente_id)    
            
        if request.POST.get('planta'):
            planta_id = int(request.POST['planta'])
            if planta_id > 0:
                planta = Planta.objects.get(pk=planta_id)    
            
        if request.POST.get('tiempo_estimado'):
            tiempo_estimado = request.POST['tiempo_estimado']
            
        if request.POST.get('correos_contacto'):
            correos_contacto = request.POST['correos_contacto']            
            
        # Re`gistro de cambios en los datos del rondin    
        try:   
            go = Rondin.objects.create(
                nombre=nombre,
                admin_aguilas=admin_aguilas,
                cliente=cliente,
                planta=planta,
                tiempo_estimado=tiempo_estimado,
                correos_contacto=correos_contacto                
            )
            messages.add_message(request,  messages.SUCCESS, 'Rondín creado exitosamente')
        except Exception as e:
            go = None        
            print(e)
            messages.add_message(request,  messages.ERROR, 'No se creo el Rondón, hubo un error')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_rondines_rondin_create')          
    
    return render(request, 'administrador/rondines/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'clientes': clientes, 'plantas': plantas, 'guardias': guardias, 'rondines': rondines, 'rondin_id': rondin_id })

# Carga por AJAX de los Rondines de una Unidad de Negocio
def ajax_load_rondines_de_planta(request):
    planta_id = request.GET.get('planta_id')    
    crondines_planta = Rondin.objects.filter(planta_id=planta_id)        
    return render(request, 'administrador/options/crondines_de_planta_dropdown_options.html', {'crondines_planta': crondines_planta})

# Carga por AJAX de los Rondines de un Unidad de Negocio
def ajax_load_puntos_de_rondin(request):
    rondin_id = request.GET.get('rondin_id')    
    cpuntos_rondin = Punto.objects.filter(rondin_id=rondin_id, activo = True)    
    rondin = Rondin.objects.get(pk=rondin_id)    
        
    return render(request, 'administrador/options/cpuntos_de_rondin_dropdown_options.html', {'cpuntos_rondin': cpuntos_rondin, 'planta_lat': rondin.planta.lat, 'planta_lng': rondin.planta.lng })

# Desactiva el punto especifico por AJAX, en base al id de rondin
def ajax_desactivar_punto(request):
    punto_id = request.GET.get('punto_id')    
    
    try:               
        punto = Punto.objects.get(pk=punto_id)
        punto.activo = False
        go = punto.save(update_fields=['activo'])
        vreturn = True        
    except Exception as e:        
        #print(e)
        vreturn = False
        
    return render(request, 'administrador/options/cdesactivar_punto_options.html', {'vreturn': vreturn })

# Agrega o modifica el punto ingresado en la DB Panoptic
def ajax_agregar_mod_punto(request):
    
    punto_id = request.GET.get('punto_id')
    punto_lat = request.GET.get('punto_lat')
    punto_lng = request.GET.get('punto_lng')    
    punto_nombre = request.GET.get('punto_nombre')
    punto_tareas = request.GET.get('punto_tareas')
    punto_rondin_id = request.GET.get('punto_rondin_id')    
    
    try:
        #Si existe el punto procede a su actualización                   
        if punto_id != '':        
            
            punto = Punto.objects.get(pk=punto_id, activo=True)
            punto.lat=punto_lat
            punto.lng=punto_lng
            punto.activo=True
            punto.nombre=punto_nombre    
            punto.tareas=punto_tareas        
            punto.rondin_id =punto_rondin_id        
            punto.save(update_fields=['lat', 'lng', 'nombre', 'tareas', 'activo'])
            vreturn = 'actualizado'                  
        
        else:           
            
            rondin = Rondin.objects.get(pk=punto_rondin_id)            
            punto = Punto.objects.create(orden=1, lat=punto_lat, lng=punto_lng, nombre=punto_nombre, activo=True, rondin=rondin, tareas=punto_tareas)
            punto.save        
            vreturn = 'creado'                    
            
    except Punto.DoesNotExist:           
        print('error')
        
    print(vreturn)
    return render(request, 'administrador/options/cagregar_mod_punto_options.html', {'vreturn': vreturn })

# Carga por AJAX de las Tareas de una Unidad de Negocio
def ajax_load_tareas_de_rondin(request):
    rondin_id = request.GET.get('rondin_id')    
    cpuntos_rondin = Punto.objects.filter(rondin_id=rondin_id, activo = True)    
    rondin = Rondin.objects.get(pk=rondin_id)    
        
    return render(request, 'administrador/options/ctareas_de_planta_dropdown_options.html', {'cpuntos_rondin': cpuntos_rondin, 'planta_lat': rondin.planta.lat, 'planta_lng': rondin.planta.lng })

# Carga por AJAX de las Evidencias de algún Rondín
def ajax_load_evidencias_de_rondin(request):
    rondin_id = request.GET.get('rondin_id')    
    evidencias = EvidenciaPunto.objects.all()
    #de esa planta
    evidencias2 = EvidenciaPunto.objects.filter(rondinhecho__guardia_id=15)
    evidencias3 = EvidenciaPunto.objects.filter(rondinhecho__hora_inicio__contains='2020-04-24')
    #rondin = Rondin.objects.get(pk=rondin_id)        
        
    return render(request, 'administrador/options/cevidencias_de_rondin_dropdown_options.html', {'evidencias': evidencias3 })
    
# Block Editar Rondin
def admin_rondines_rondin_block_edit(request, rondin_id): 
    userdict = user_validation.validate(request) 
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all()    
    guardias = User.objects.filter(role__alias_rol="guardia")
    rondines = Rondin.objects.all().order_by('-id')[:5]
    
    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'datepicker', 'wickedpicker', 'fancybox', 'taginput']
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables',  'js_taginput', 'js_form_validator', 'js_moment', 'js_datepicker' , 'js_wickedpicker',  'js_mapa_interactivo']     
    
    # SI la forma fue enviada, se procesan los datos            
    if request.method == 'POST':
        
        rondin = Rondin.objects.get(pk=rondin_id )   
        
        if request.POST.get('nombre'):
            rondin.nombre = request.POST['nombre']
            
        if request.POST.get('admin_aguilas'):
            aguilas_id = int(request.POST['admin_aguilas'])
            if aguilas_id > 0:
                rondin.admin_aguilas = User.objects.get(pk=aguilas_id) 
            
        if request.POST.get('cliente'):
            cliente_id = int(request.POST['cliente'])
            if  cliente_id> 0:
                rondin.cliente = Cliente.objects.get(pk=cliente_id)    
            
        if request.POST.get('planta'):
            planta_id = int(request.POST['planta'])
            if planta_id > 0:
                rondin.planta = Planta.objects.get(pk=planta_id)    
            
        if request.POST.get('tiempo_estimado'):
            rondin.tiempo_estimado = request.POST['tiempo_estimado']
            
        if request.POST.get('correos_contacto'):
            print(request.POST['correos_contacto'] );
            rondin.correos_contacto = request.POST['correos_contacto']            
            
        # Registro de cambios en los datos del rondin    
        try:               
            go = rondin.save(update_fields=['nombre', 'admin_aguilas', 'cliente', 'planta', 'tiempo_estimado', 'correos_contacto'])
            messages.add_message(request,  messages.SUCCESS, 'Rondín modificado exitosamente')
        except Exception as e:
            go = None        
            print(e)
            messages.add_message(request,  messages.ERROR, 'No se modificó el rondín, hubo un error.')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_rondines_rondin_create')          
    
    return render(request, 'administrador/rondines/create.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'clientes': clientes, 'plantas': plantas, 'guardias': guardias, 'rondines': rondines })

#AJAX Regresa registro de rondin
@api_view(["GET"])
def ajax_load_rondin(request):
    def initialize_request(self, request, *args, **kwargs):
        if not isinstance(request, Request):
            request = super().initialize_request(request, *args, **kwargs)
        return request
 
    rondin_id = request.GET.get('rondin_id')    
    rondin = Rondin.objects.get(pk=rondin_id)    
    print(rondin)    
    
    serializer = RondinSerializer(rondin)
    return Response(serializer.data)    

def admin_rondines_mapa_interactivo(request): 
    userdict    = user_validation.validate(request) 
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_mapa_interactivo', 'js_wickedpicker']       
    
    return render(request, 'administrador/rondines/mapainteractivo.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict })

def admin_rondines(request): 
    userdict    = user_validation.validate(request) 
    rondines   = Rondin.objects.all()
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_mapa_interactivo']       
    
    return render(request, 'administrador/rondines/listado.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'rondines': rondines })

def admin_rondines_qr(request): 
    userdict = user_validation.validate(request) 
    
    rondines = Rondin.objects.all()    
    
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_mapa_interactivo']       
    
    if request.method == 'POST':
        
        try:
            rondin_id = request.POST['rondin_id']
            rondin = Rondin.objects.get(pk = rondin_id)        
            #puntos = rondin.punto_set.all()                  
            puntos = Punto.objects.filter(rondin_id = rondin.id,).filter(activo = 1)
          
        except KeyError:
            rondin_id = 0  
            
        return render(request, 'administrador/rondines/impresion_qrs.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'rondines': rondines, 'rondin_id': rondin_id, 'puntos': puntos, 'rondin': rondin })  
    
    return render(request, 'administrador/rondines/impresion_qrs.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'rondines': rondines })

def admin_rondines_resumen(request):  
    userdict = user_validation.validate(request) 
    rondines = Rondin.objects.all()
    ultimos_rondines = Rondin.objects.all()[:5]
    puntos = Punto.objects.all()[:5]
    punto_hechos = PuntoHecho.objects.all()[:5]    
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]       
    
    return render(request, 'administrador/rondines/resumen.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'rondines': rondines, 'ultimos_rondines': ultimos_rondines, 'puntos': puntos,  'punto_hechos': punto_hechos })

def admin_rondines_show(request, rondin_id):
    userdict = user_validation.validate(request)    
    rondinToShow = Rondin.objects.get(pk= rondin_id ) 

    puntos_rodin = Punto.objects.filter(rondin_id=rondinToShow.id,activo=1).all()  
     
    return render(request, 'administrador/rondines/show.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'rondin': rondinToShow, 'puntos_rodin': puntos_rodin })

def admin_rondines_geocerca(request, un_id):
    userdict = user_validation.validate(request)
    planta = Planta.objects.get(pk= un_id )   
    print(planta.nombre)        
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_geocerca_show', 'js_wickedpicker', 'js_fancybox']           
  
    return render(request, 'administrador/rondines/geocerca.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'planta': planta })

def admin_rondines_geocerca_edit(request, un_id):
    userdict = user_validation.validate(request)
    planta = Planta.objects.get(pk= un_id )       
    
    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_geocerca', 'js_wickedpicker', 'js_fancybox']           
    
    # SI la forma fue enviada, se procesan los datos            
    if request.method == 'POST':
        if request.POST.get('polyradio'):
            planta.polyradio = request.POST['polyradio']        
            
        # Registro de cambios en los datos del usuario    
        try:   
            go = planta.save() 
            messages.add_message(request,  messages.SUCCESS, 'Geocerca de Unidad de Negocio asignada exitosamente')
        except Planta.DoesNotExist:
            go = None        
            messages.add_message(request,  messages.ERROR, 'No se modifcó la Unidad de Negocio, hubo un error.')
        
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del usuario 
        return redirect('administrador:admin_rondines_geocerca_edit', un_id=un_id)        
  
    return render(request, 'administrador/rondines/geocerca_edit.html', { 'css_list': css_list, 'js_list': js_list, 'userdict': userdict, 'planta': planta })

def admin_rondines_reportes(request):
    clientes = Cliente.objects.all()
    plantas = Planta.objects.all() 
    
    return render(request, 'administrador/rondines/reporte_general.html', { 'css_list': css_list, 'js_list': js_list, 'clientes': clientes, 'plantas': plantas })

# Generación de reporte via AJAX de Rondines y puntos realizados
def ajax_load_reporte_rondin(request):
    cliente_id = request.GET.get('cliente_id')   
    planta_id = request.GET.get('planta_id')   
    fec_inicio = request.GET.get('fec_inicio')   
    fec_fin = request.GET.get('fec_fin')
        
    #Obtener set de rondines hecho bajo los criterios especificados     
    rondinesHechos = RondinHecho.objects.filter(rondin__cliente_id=cliente_id, rondin__planta_id=planta_id, hora_inicio__gte=fec_inicio, hora_fin__lte=fec_fin)

    evidenciasP = EvidenciaPunto.objects.filter(rondinhecho__in=rondinesHechos)
    print(evidenciasP)
    
    #Obtener los puntos hechos durante tal periodo, cliente y planta
    #puntosHecho = PuntoHechoSerializer(many=True, rondinesHechos)    
        
    return render(request, 'administrador/options/rep_rondines_listado.html', {'rondines': rondinesHechos, 'evidenciasP': evidenciasP })
    
# Generación puntos realizados en base al ID de rondin hecho
def ajax_load_reporte_puntos_hechos(request):
    rondin_hecho_id = request.GET.get('rondin_hecho_id')       
    #print('Entro a Puntos hechos!!')
    #print('ID de rondin hecho es:')
    #print(rondin_hecho_id)
    #Obtener set de puntos realizados del ID del rondin hecho
    puntos_hechos = PuntoHecho.objects.filter(rondinhecho__id=rondin_hecho_id)
    puntos_hechos2 = PuntoHecho.objects.filter(rondinhecho__id=rondin_hecho_id).count()    
    #print(puntos_hechos)      
    #print(puntos_hechos2)      
        
    return render(request, 'administrador/options/rep_rondines_puntos_hecho.html', {'puntos': puntos_hechos })

# Generación evidencias en base a rondin hecho ID y punto ID
def ajax_load_reporte_evidencias_de_puntos_hechos(request):
    rondinhecho_id = request.GET.get('rondinhecho_id')
    puntohecho_id = request.GET.get('puntohecho_id')
    punto_id = request.GET.get('punto_id')    
    
    #print('Data de Evidencias')    
    #print(rondinhecho_id)
    #print(puntohecho_id)
    #print(punto_id)

    #Obtener set de evidencias
    evidencias = EvidenciaPunto.objects.filter(rondinhecho__id=rondinhecho_id, punto__id=punto_id)    
        
    return render(request, 'administrador/options/rep_rondines_evidencias_de_puntos_hechos.html', {'evidencias': evidencias})
    

# Generación evidencias en base a rondin hecho ID y punto ID
def ajax_load_reporte_grafica_puntos_hechos2(request):
    rondinhecho_id = request.GET.get('rondinhecho_id')
    puntohecho_id = request.GET.get('puntohecho_id')
    punto_id = request.GET.get('punto_id')    
    
    #print('Data de Evidencias')    
    #print(rondinhecho_id)
    #print(puntohecho_id)
    #print(punto_id)

    #Obtener set de evidencias
    evidencias = EvidenciaPunto.objects.filter(rondinhecho__id=rondinhecho_id, punto__id=punto_id)    
        
    return render(request, 'administrador/options/rep_rondines_evidencias_de_puntos_hechos.html', {'evidencias': evidencias })
