from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse
from core.models import Planta, Cliente, User, Role, Notificacion
from ddmanagement.models import Movimiento, Vehiculo
from analytics.models import F_18_puntos_Trailer
from django.core import serializers
import json
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
import datetime as dt
from core import notifications
import pytz

# Vistas de movimientos en Dashboard de Administrador
def ajax_lista_movimientos(request):    
    planta = request.GET.get('planta')
    startMain = request.GET.get('start')    
    endMain = request.GET.get('end')    
       
    timezone = pytz.timezone('America/Chihuahua')
    
    startMain_obj = dt.datetime.strptime(startMain, '%Y-%m-%d %H:%M')
    startMain = timezone.localize(startMain_obj)
    
    endMain_obj = dt.datetime.strptime(endMain, '%Y-%m-%d %H:%M')
    endMain = timezone.localize(endMain_obj)    
    
    start = startMain.date()
    end = endMain.date()     
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        dataset = Movimiento.objects.filter(planta=objPlanta).filter(fecha__range=(str(start), str(end)))
    else:
        dataset = Movimiento.objects.filter(fecha__range=[str(start), str(end)])
    
    data=serializers.serialize ("json", dataset, use_natural_foreign_keys=True)
    
    return JsonResponse(data, safe=False)


def ajax_en_tiempo_movimientos(request):    
    planta = request.GET.get('planta')
    startMain = request.GET.get('start')    
    endMain = request.GET.get('end')    
       
    timezone = pytz.timezone('America/Chihuahua')
    
    startMain_obj = dt.datetime.strptime(startMain, '%Y-%m-%d %H:%M')
    startMain = timezone.localize(startMain_obj)
    
    endMain_obj = dt.datetime.strptime(endMain, '%Y-%m-%d %H:%M')
    endMain = timezone.localize(endMain_obj)    
    
    start = startMain.date()
    end = endMain.date() 
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        total = Movimiento.objects.filter(planta=objPlanta).filter(fecha__range=[str(start), str(end)]).count()
        entiempo = Movimiento.objects.filter(planta=objPlanta).filter(fecha__range=[str(start), str(end)]).filter(ef=1).count()
        fueratiempo = Movimiento.objects.filter(planta=objPlanta).filter(fecha__range=[str(start), str(end)]).filter(ef=0).count()
    else:
        total = Movimiento.objects.filter(fecha__range=[str(start), str(end)]).count()
        entiempo = Movimiento.objects.filter(fecha__range=[str(start), str(end)]).filter(ef=1).count()
        fueratiempo = Movimiento.objects.filter(fecha__range=[str(start), str(end)]).filter(ef=0).count()
        
    to_json = {
        "total": total,
        "entiempo": entiempo,
        "fueratiempo": fueratiempo
    }
    return JsonResponse(to_json, safe=False)
    #return HttpResponse(simplejson.dumps(to_json), mimetype='application/json')
    
def ajax_lista_valorcarga(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    #planta_id = request.GET.get('planta_id')
    #movimientos = Movimiento.objects.filter(planta_id=planta_id, fecha__range=[start, end]).all()
    
    a = datetime.strptime(start, "%Y-%m-%d")
    b = datetime.strptime(end, "%Y-%m-%d")

    sJson = "["
    coma = ""

    for dt in rrule(DAILY, dtstart=a, until=b):
        print(dt.strftime("%Y-%m-%d"))
        tval = 0
        movimientos = Movimiento.objects.filter(fecha__contains=dt.strftime("%Y-%m-%d")).all()
        for m in movimientos:
            val = float(m.valor_carga)
            tval += val 
            print(str(m.fecha.strftime("%Y-%m-%d"))+" - "+str(val))

        sJson += coma+'{"fecha": "'+dt.strftime("%Y-%m-%d")+'", "valor": '+str(tval)+'}'
        coma = ","

    sJson += "]" 

    return HttpResponse(sJson)

def ajax_charts_activos_movimientos(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)
    
    dias=[]
    concluidos=[]
    activos=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            concluido = Movimiento.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(confirmacion=True).count()
            concluidos.append(concluido) 
                        
            activo = Movimiento.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(confirmacion=False).exclude(fecha_fin=None).count()
            activos.append(activo) 
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            concluido = Movimiento.objects.filter(fecha__date=start).filter(confirmacion=True).count()
            concluidos.append(concluido) 
            
            activo = Movimiento.objects.filter(fecha__date=start).filter(confirmacion=False).filter(fecha_fin=None).count()
            activos.append(activo) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "concluidos": concluidos,
    "activos": activos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_valor_movimientos(request):    
    planta = request.GET.get('planta')
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date() 
    
    #print(start)
    #print(end)
    
    delta = dt.timedelta(days=1)
    
    dias=[]
    valores=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            valor = list(Movimiento.objects.filter(planta=objPlanta).filter(fecha__date=start).aggregate(Sum('valor_carga')).values())[0]
            valores.append(valor) 
            print(start)
            print(valor)
            
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:        
        
        
        while start <= end:
            valor = list(Movimiento.objects.filter(fecha__date=start).aggregate(Sum('valor_carga')).values())[0]
            valores.append(valor) 
            print(start)
            print(valor)
            # field = 'evidencia_defensa'
            # lookup = "%s__isnull" % field        
            # records = F_18_puntos_Trailer.objects.filter(fecha__date=start).filter(**{ lookup: False}).count()
            
            # print('Records')
            # print(records)
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta            

    to_json = {
    "dias": dias,
    "valores": valores
    }
    
    return JsonResponse(to_json, safe=False)
    
def ajax_fuera_ruta(request):
    movimiento_id = request.GET.get('movimiento_id')
    #movimiento = url 'administrador:admin_movimientos_detalle' movimiento_id=movimiento_id 
     
    if Movimiento.objects.filter(pk=movimiento_id).filter(confirmacion=False).exists():
        print('Existe el movimiento '+str(movimiento_id))
        #param_bol => Si esta fuera de rita es True
        if not Notificacion.objects.filter(idproblema=movimiento_id).filter(modelo='Movimiento').filter(param_bol=True).exists():
            
            print('Guardando notificacion')    
            dMov = Movimiento.objects.get(pk=movimiento_id)            
            notificacion = Notificacion(titulo='Fuera de ruta', mensaje='La unidad '+dMov.vehiculo.placas+' Mov. ID: '+str(dMov.id),idproblema= movimiento_id, modelo='Movimiento', param_bol=True)
            notificacion.save()            
            
        else:
            print('Existe la notificacion Hoy')               
            #hora_actual = dt.datetime.now()
            hora_actual = timezone.now()
            # Verificar que haya pasado 30 minutos y aun esté fuera de ruta
            #Obtener fecha de Movimiento
            mov = Notificacion.objects.filter(idproblema=movimiento_id).order_by('-fecha').first()
            #print('Que hay en MOV'+ str(movimiento_id))
            #print(mov.fecha)
            #print('Hora de Última Notificacion')
            #print(mov.fecha.minute)
            #print('Hora de sistema de Servidor')
            #print(hora_actual)
            dif = hora_actual - mov.fecha
            #print('Diferencia')
            #print(dif)
            #print(hora_actual.minute)
            #print('*********** Comparando *************')
            dif_hours = hora_actual.hour - mov.fecha.hour           
            dif_minutes = hora_actual.minute - mov.fecha.minute
            
            #print('dif_hours')
            #print(dif_hours)
            #print('dif_minutes')
            #print(dif_minutes)
            
            #if dif_hours >= 1 or dif_minutes > 5:
                #hace nueva notificacion 
                #print('Se excedió')
                #print('Guardando notificacion al exceder')    
               
            
            
            noti = Notificacion()
            noti.titulo = "Movimiento fuera de ruta"
            noti.mensaje = "La unidad se ha salido de ruta del movimiento  "+dMov.vehiculo.placas+" Mov. ID:  "+str(dMov.id)
            noti.modelo = "Movimiento"
            noti.idproblema = dMov.id
            noti.param_bol = False
            noti.usuario_id = request.user.id
            noti.save()
            
            try:
                print("mandar notificación")
                notifications.sendemailsbyplanta("Fuera de  ruta", "El vehículo ha salido de ruta", dMov.planta, "ddmanagement", notificacion)
            except Exception as error2:
                print("No se pudo enviar notificación: "+str(error2))
            #else:
             #   print('Dentro del limite')
            
    else:
        #print('No existe el movimiento '+str(movimiento_id))
        movimiento_id = 0
        
    to_json = {
    "movimiento": movimiento_id
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_dentro_ruta(request):
    movimiento_id = request.GET.get('movimiento_id')
    #movimiento = url 'administrador:admin_movimientos_detalle' movimiento_id=movimiento_id 
    dMov = Movimiento.objects.get(pk=movimiento_id)   
    notificacion = Notificacion(titulo='Fuera de ruta *', mensaje='La unidad '+dMov.vehiculo.placas+' Mov. ID: '+str(dMov.id),idproblema= movimiento_id, modelo='Movimiento', param_bol=True)
    notificacion.save()            
    if Movimiento.objects.filter(pk=movimiento_id).filter(confirmacion=False).exists():        
        #param_bol => Si esta fuera de rita es True
        if not Notificacion.objects.filter(idproblema=movimiento_id).filter(modelo='Movimiento').filter(param_bol=False).exists():
            
            noti = Notificacion()
            noti.titulo = "Movimiento dentro de ruta"
            noti.mensaje = "La unidad esta dentro de la ruta del movimiento  "+dMov.vehiculo.placas+" Mov. ID:  "+str(dMov.id)
            noti.modelo = "Movimiento"
            noti.idproblema = dMov.id
            noti.param_bol = False
            noti.usuario_id = request.user.id
            noti.save()
            
            try:
                print("mandar notificación")
                notifications.sendemailsbyplanta("Dentro  de  ruta", "El vehículo esta dentro  de ruta", dMov.planta, "ddmanagement", notificacion)
            except Exception as error2:
                print("No se pudo enviar notificación: "+str(error2))
        
    to_json = {
    "movimiento": movimiento_id
    }
    
    return JsonResponse(to_json, safe=False) 
    
def ajax_mov_info_esn(request):
    esn = request.GET.get('esn')
    mov = Movimiento.objects.filter(vehiculo__gpsdevice__deviceesn=esn).filter(confirmacion=False).order_by('-id').first()
    veh = Vehiculo.objects.filter(gpsdevice__deviceesn=esn).first()
    
    if mov != None:
        if mov.chofer.imagen:
            foto = mov.chofer.imagen.url
        else:
            foto = None    
            
        to_json = {
            "id": mov.id,
            "esn": esn,
            "estatus": mov.estatus,
            "nombre": mov.nombre,
            "matricula": veh.placas,
            "origen": mov.origen,
            "destino": mov.destino,
            "emp_transp": mov.emp_transp.nombre,
            "foto": foto
        }
    else:
        to_json = {
            "id": 0
        }
        
    return JsonResponse(to_json, safe=False) 
    
def ajax_heatmap_movs_activos(request):
    #Param planta_id
    planta_id = request.GET.get('planta_id')    
    planta = Planta.objects.get(pk=planta_id)
    mov_activos = Movimiento.objects.filter(planta=planta).filter(confirmacion=True).filter(ef=False).order_by('-id')[:5]   
    mov_activos_s = json.loads(serializers.serialize("json",mov_activos))
    
    if mov_activos!=None:
        to_json = {
            "movs_activos": mov_activos_s
        }
    else:
        to_json = {
            "id": 'Iniciado Heatmap MOvs Activos: Resultando None'
        }   
        
    return JsonResponse(to_json, safe=False) 

def ajax_heatmap_movs_finalizados(request):
    #Param planta_id
    planta_id = request.GET.get('planta_id')    
    planta = Planta.objects.get(pk=planta_id)    
    mov_finalizados = Movimiento.objects.filter(planta=planta).filter(confirmacion=True).filter(ef=True).order_by('-id') [:5] 
    mov_finalizados_s = json.loads(serializers.serialize("json",mov_finalizados))
    
    if mov_finalizados!=None:
        to_json = {
            "movs_finalizados": mov_finalizados_s
        }
    else:
        to_json = {
            "id": 'Iniciado Heatmap MOvs Finalizados: Resultando None'
        }   
        
    return JsonResponse(to_json, safe=False) 

def ajax_heatmap_inc_viales(request):
    #esn = request.GET.get('esn')
    #mov = Movimiento.objects.filter(vehiculo__gpsdevice__deviceesn=esn).filter(confirmacion=False).order_by('-id').first()
    #veh = Vehiculo.objects.filter(gpsdevice__deviceesn=esn).first()  

    to_json = {
        "id": 'Iniciado Heatmap Incidentes Viales'
    }
        
    return JsonResponse(to_json, safe=False) 