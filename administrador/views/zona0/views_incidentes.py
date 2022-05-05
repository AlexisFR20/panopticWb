from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente, TipoIncidente
from core.models import Planta, Cliente, User, Role, Region, Sucursal, Ciudad, Notificacion
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import auth, messages
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import datetime 
import json
from django.core import serializers
from django.db.models import Count
from django.db import connection


from core import notifications
from core.externalModels import CiaaR1

n = Notificacion.objects.filter(visto = False)

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']

js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_clipboard', 'js_fancybox' ]

def admin_incidentes_dash(request):  

    cliente = request.user.cliente    
    if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
        plantas = Planta.objects.filter(cliente=cliente)
    else:
        nombreplanta = request.user.planta       
        plantas = Planta.objects.filter(nombre=nombreplanta)  

    incidentes = Incidente.objects.all()  
    #plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    tipo_incidentes = TipoIncidente.objects.all()  
    ciudades = Ciudad.objects.all()  
    notificaciones = n 

    cliente = request.user.cliente
    plantas_v = Planta.objects.get(nombre=nombreplanta) 
    
    return render(request, 'administrador/zona0/incidentes/dashboard.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'tipo_incidentes': tipo_incidentes, 'ciudades': ciudades, 'vcliente': cliente, 'vplantas': plantas_v, 'notificaciones': notificaciones  })

def admin_incidentes_ajax(request):    
    vciudad = request.GET.get('vciudad')
    vstart = request.GET.get('vstart')
    vend = request.GET.get('vend')
    #print("************")
    #print(vciudad)
    #print("************")
    #print(vstart)
    #print("************")
    #print(vend)
    #print("************")
    try:
        
        #go = list(Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')).filter(fecha='2019-12-24') )
        if vciudad == None:     
            total_incidentes = Incidente.objects.count()
            incidentes = list(Incidente.objects.all())
            go = list(Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')) )
            obj_incidentes = {
                "Res": 'OK',
                "Total_Incidentes": total_incidentes,
                "Totales": go,
                "Incidente": incidentes
            }
        else:
            incidentes = Incidente.objects.filter(fecha__range=(vstart, vend)).all()

            incidentes = json.loads(serializers.serialize("json",incidentes))
            
            total_incidentes = Incidente.objects.filter(ciudad=vciudad).count()
            #go = list( Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')).filter(ciudad=ciudad).order_by('tipo') )

            if vstart != None and vend != None:
                rdates = ' AND m.fecha >= "' + vstart + '" AND m.fecha <= "' + vend + '"'
            else:
                rdates = ""
            
            #print('SELECT k.nombre, k.alias, COUNT(m.tipo) AS dcount FROM panoptic_iotrem.entorno_tipoincidente k LEFT JOIN panoptic_iotrem.entorno_incidente m ON m.tipo = k.alias AND m.ciudad = "' + vciudad + '"' + rdates + ' GROUP BY k.nombre') 
            cursor = connection.cursor()
            #cursor.execute('SELECT k.nombre, k.alias, COUNT(m.tipo) AS dcount, AVG(DATEDIFF( DATE_ADD(m.fecha,INTERVAL 7 DAY), m.fecha )) AS promedio FROM panoptic_iotrem.entorno_tipoincidente k LEFT JOIN panoptic_iotrem.entorno_incidente m ON m.tipo = k.alias AND m.ciudad = "' + vciudad + '"' + rdates + ' GROUP BY k.nombre') 
            cursor.execute(
                'SELECT '+
                '    k.nombre, ' +
                '    k.alias,    ' +
                '    COUNT(m.tipo) AS dcount,' +
                '    (' +
                '        SELECT ' +
                '            COUNT(mm.tipo) AS Feb' +
                '        FROM' +
                '            mxpanoptic.entorno_incidente mm' +
                '        WHERE' +
                '            mm.fecha >= DATE_SUB("'+vstart+'",INTERVAL 7 DAY) AND mm.fecha <= "'+vstart+'" AND mm.ciudad = "'+vciudad+'" AND mm.tipo = k.alias' +
                '    ) AS dcount2    ' +
                ' FROM ' +
                '    mxpanoptic.entorno_tipoincidente k ' +
                'LEFT JOIN ' +
                '    mxpanoptic.entorno_incidente m ON m.tipo = k.alias AND m.ciudad = "'+vciudad+'" AND m.fecha >= "'+vstart+'" AND m.fecha <= "'+vend+'" ' +
                'GROUP BY ' +
                '    k.nombre'
            )

            
            go = cursor.fetchall()
            #print(go)
            #go = Incidente.objects.filter(ciudad=ciudad).count()
            obj_incidentes = {
                "Res": 'OK',
                "Total_Incidentes": total_incidentes,
                "Totales": go,
                "Incidente": incidentes
            }

    except Incidente.DoesNotExist:
        go = None
        incidentes = None
        obj_incidentes = {
            "Res": 'ERROR',
            "Total_Incidentes": '0',
            "Totales": go,
            "Incidente": incidentes
        }        
        #messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')

    return JsonResponse(obj_incidentes, safe=False)


        
def admin_incidentes_index(request):    
    incidentes = Incidente.objects.order_by('-id').all()
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()  
    notificaciones = n 
    return render(request, 'administrador/zona0/incidentes/index.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'notificaciones': notificaciones })

def admin_incidentes_agrupado(request):    
    incidentes = Incidente.objects.all()  
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()  
    notificaciones = n 
    return render(request, 'administrador/zona0/incidentes/agrupado-tipo.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'notificaciones': notificaciones })
    
def admin_incidentes_agrupado_ciudad(request):    
    incidentes = Incidente.objects.all()  
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()  
    notificaciones = n 
    return render(request, 'administrador/zona0/incidentes/agrupado-ciudad.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'notificaciones': notificaciones })
    
def admin_incidentes_create(request):

    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'gigo']

    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_gigo' ]

    itipos = TipoIncidente.objects.all().order_by('nombre')
    ciudades = Ciudad.objects.all();
    notificaciones = n
    d = datetime.time(16, 33, 45)
    
    print(d)
    
    if request.method == 'POST':
        
       
        # Si se envío la forma vía get simplemente se muestra el formulario de crear del incidente 
        if request.POST.get('user'):
            cuser = request.POST['user']
            user = User.objects.get(pk=int(cuser))

        if request.POST.get('tipo'):
            tipo = request.POST['tipo']
            tipor = TipoIncidente.objects.get(alias=tipo)

        if request.POST.get('titulo'):
            titulo = request.POST['titulo']

        if request.POST.get('descripcion'):
            descripcion = request.POST['descripcion']

        if request.POST.get('direccion'):
            direccion = request.POST['direccion']

        if request.POST.get('lat'):
            lat = request.POST['lat']

        if request.POST.get('lng'):
            lng = request.POST['lng']

        if request.POST.get('estado'):
            estado = request.POST['estado']

        if request.POST.get('pais'):
            pais = request.POST['pais']

        if request.POST.get('nivel'):
            nivel = request.POST['nivel']

        if request.POST.get('url_noticia'):
            url_noticia = request.POST['url_noticia']

        if request.POST.get('cantidad'):
            cantidad = request.POST['cantidad']

        if request.POST.get('fecha_real'):
            fecha = request.POST['fecha_real']

        if request.POST.get('hora'):
            hora = request.POST['hora']

        if request.POST.get('ciudad'):
            ciudad = request.POST['ciudad']

        if request.POST.get('estado'):
            estado = request.POST['estado']

        if request.POST.get('pais'):
            estado = request.POST['pais']
        
        #pais = 'México'               

         # Registro de cambios en los datos del tipo de incidente    
        try:   
            incidente = Incidente.objects.create(
                tipor = tipor,
                tipo = tipo,
                titulo = titulo,
                descripcion = descripcion,
                direccion = direccion,
                lat = lat,
                lng = lng,
                nivel = nivel,
                url_noticia = url_noticia,
                cantidad = cantidad,
                fecha = fecha,
                hora = hora,
                ciudad = ciudad,
                estado = estado,
                pais = pais,
                user = user
            )
            if cuser:
                incidente.save()           
        
            messages.add_message(request, messages.SUCCESS, 'Incidente creado exitosamente')
            return redirect('administrador:admin_incidentes_index')      
        except Incidente.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el Incidente, hubo un error.')        
        
        return redirect('administrador:admin_incidentes_index')     
    
    return render(request, 'administrador/zona0/incidentes/create.html', {'css_list': css_list, 'js_list': js_list, 'itipos': itipos, 'ciudades': ciudades, 'notificaciones': notificaciones })

def admin_incidentes_edit(request, inc_id):

    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'gigo']

    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_gigo' ]

    itipos = TipoIncidente.objects.all().order_by('nombre')  
    ciudades = Ciudad.objects.all();
    notificaciones = n
    try:
        incidente = Incidente.objects.get(pk=inc_id)
    except:        
        incidente = None

    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del incidente 
        if request.POST.get('tipo'):
            intTipo = int(request.POST['tipo'])
            if intTipo > 0:
                tipoIncidente = TipoIncidente.objects.get(pk=intTipo)
                incidente.tipor = tipoIncidente
                incidente.tipo = tipoIncidente.alias

        
        if request.POST.get('nivel'):
            incidente.nivel = request.POST['nivel']
            
        if request.POST.get('descripcion'):
            incidente.descripcion = request.POST['descripcion']
            
        if request.POST.get('url_noticia'):
            incidente.url_noticia = request.POST['url_noticia']
            
        if request.POST.get('cantidad'):
            incidente.cantidad = request.POST['cantidad']
        
        # Registro de cambios en los datos del incidente    
        try:   
            go = incidente.save()            
            messages.add_message(request,  messages.SUCCESS, 'Incidente modificado exitosamente')
        except Incidente.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el registro del Incidente, hubo un error.')
            
        return redirect('administrador:admin_incidentes_edit', inc_id=inc_id)          
    
    return render(request, 'administrador/zona0/incidentes/edit.html', { 'css_list': css_list, 'js_list': js_list, 'incidente': incidente, 'itipos': itipos, 'ciudades': ciudades, 'notificaciones': notificaciones })

def admin_incidentes_delete(request, inc_id):
    notificaciones = n
    try:
        go = Incidente.objects.filter(id=inc_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'El Incidente ha sido borrado exitosamente')
    except TipoIncidente.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró el Incidente, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_incidentes_index')
    
def admin_incidentes_tipos(request):    
    tipos = TipoIncidente.objects.all()  
    notificaciones = n
    return render(request, 'administrador/zona0/incidentes/tipos/index.html', { 'css_list': css_list, 'js_list': js_list, 'tipos':tipos, 'notificaciones': notificaciones })

def admin_incidentes_tipos_create(request):
    notificaciones = n
    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de crear del tipo de incidente 
        if request.POST.get('nombre'):
            nombre = request.POST['nombre']

        if request.POST.get('alias'):
            alias = request.POST['alias']      

         # Registro de cambios en los datos del tipo de incidente    
        try:   
            tipo = TipoIncidente.objects.create(
                nombre = nombre,
                alias = alias
            )
            tipo.save()

            # Almacenamiento del archivo de imagen, en el caso de haberse agregado
            icono = request.FILES.get('icono', False)     
            if icono:                
                if settings.DEBUG:
                    fs = FileSystemStorage(location='media/iconos/')                
                else:
                    fs = FileSystemStorage(location='/home/ubuntu/pgit/iconos/avatars/')                        
                
                #fs = FileSystemStorage(location='/home/ubuntu/pgit/media/iconos/')                        
                filename = fs.save(icono.name, icono)                
                tipo.icono = 'iconos/' + filename
                tipo.save()

            messages.add_message(request, messages.SUCCESS, 'Tipo de Incidente creado exitosamente')
            return redirect('administrador:admin_incidentes_tipos')      
        except TipoIncidente.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el Tipo de Incidente, hubo un error.')
            
        return redirect('administrador:admin_incidentes_tipos')     
    
    return render(request, 'administrador/zona0/incidentes/tipos/create.html', {'css_list': css_list, 'js_list': js_list })

def admin_incidentes_tipos_edit(request, tipo_id):
    notificaciones = n
    try:
        tipo = TipoIncidente.objects.get(pk=tipo_id)
    except:        
        tipo = None

    if request.method == 'POST':
        # Si se envío la forma vía get simplemente se muestra el formulario de edición del tipo de incidente 
        if request.POST.get('nombre'):
            tipo.nombre = request.POST['nombre']

        if request.POST.get('alias'):
            tipo.alias = request.POST['alias']

        # Almacenamiento del archivo de imagen, en el caso de haberse agregado
        icono = request.FILES.get('icono', False)     
        if icono:                
            if settings.DEBUG:
                fs = FileSystemStorage(location='media/iconos/')                
            else:
                fs = FileSystemStorage(location='/home/ubuntu/pgit/iconos/avatars/')                        
            
            #fs = FileSystemStorage(location='/home/ubuntu/pgit/media/iconos/')                        
            filename = fs.save(icono.name, icono)                
            tipo.icono = 'iconos/' + filename
            tipo.save() 

         # Registro de cambios en los datos del tipo de incidente    
        try:   
            go = tipo.save()            
            messages.add_message(request,  messages.SUCCESS, 'Tipo de Incidente modificado exitosamente')
        except TipoIncidente.DoesNotExist:
            go = None        
            messages.add_message(request, messages.ERROR, 'No se creó el registro del Tipo de Incidente, hubo un error.')
            
        return redirect('administrador:admin_incidentes_tipos_edit', tipo_id=tipo_id)          
    
    return render(request, 'administrador/zona0/incidentes/tipos/edit.html', { 'css_list': css_list, 'js_list': js_list, 'tipo': tipo })
    
def admin_incidentes_tipos_delete(request, tipo_id):
    notificaciones = n
    try:
        go = TipoIncidente.objects.filter(id=tipo_id).delete()
        messages.add_message(request,  messages.SUCCESS, 'Tipo de Incidente borrado exitosamente')
    except TipoIncidente.DoesNotExist:
        go = None        
        messages.add_message(request,  messages.ERROR, 'No se borró el Tipo de Incidente, probablemente no exista el id asociado')
    
    return redirect('administrador:admin_incidentes_tipos')