from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse
from core.models import Planta, Cliente, User, Role
from analytics.models import F_ES_Trailers, F_18_puntos_Trailer, F_Visitantes, EntradaVehiculo, Paqueteria, ItemEntradaMaterial, Area_Restringida, Empleado_Sin_Gafete, ItemEntradaEquipo, RecibosAlmacen, Incidentes, RondinHecho
from django.core import serializers
from django.db.models import Sum
from django.db.models import Q
from datetime import datetime
from django.utils import timezone
import datetime as dt
import pytz



def ajax_charts_numero_entradas_salidas_trailers(request):    
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
    entradas=[]
    salidas=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            entrada = F_ES_Trailers.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            entradas.append(entrada)    
                        
            salida = F_ES_Trailers.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            salidas.append(salida) 
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            entrada = F_ES_Trailers.objects.filter(entrada__date=start).count()
            entradas.append(entrada) 
            
            salida = F_ES_Trailers.objects.filter(salida__date=start).count()
            salidas.append(salida) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "entradas": entradas,
    "salidas": salidas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_revision_18_puntos(request):    
    planta = request.GET.get('planta')
    field = request.GET.get('tincidente')    
    #Dato de parámetros
    start = request.GET.get('start')    
    end = request.GET.get('end')   
    #Conversión string a date obj
    start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M')
    end = dt.datetime.strptime(end, '%Y-%m-%d %H:%M')
    #Obtencion de solo fecha
    start = start.date()
    end = end.date()     
    lookup = "%s__isnull" % field             
    delta = dt.timedelta(days=1)
    
    dias=[]
    incidentes=[]

    print(field)
    print(lookup)
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            incidente = F_18_puntos_Trailer.objects.filter(planta=objPlanta).filter(fecha__date=start).exclude(**{ lookup: True}).count()
            
            incidentes.append(incidente)    
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            incidente = F_18_puntos_Trailer.objects.filter(fecha__date=start).exclude(**{ lookup: True}).count()
            incidentes.append(incidente) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "incidentes": incidentes
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_registro_visitantes(request):    
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
    visitantes=[]
    proveedores=[]
    contratistas=[]
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:
            visitante = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo='visitante').count()
            visitantes.append(visitante)    
                        
            proveedor = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo="proveedores").count()
            proveedores.append(proveedor) 

            contratista = F_Visitantes.objects.filter(planta=objPlanta).filter(entrada__date=start).filter(tipo='contratista').count()
            contratistas.append(contratista) 
            
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            visitante = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='visitante').count()
            visitantes.append(visitante) 
            
            proveedor = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='proveedores').count()
            proveedores.append(proveedor) 

            contratista = F_Visitantes.objects.filter(entrada__date=start).filter(tipo='contratista').count()
            contratistas.append(contratista) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "visitantes": visitantes,
    "proveedores": proveedores,
    "contratistas": contratistas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_registro_vehiculos(request):    
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
    vehiculos=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            vehiculo = EntradaVehiculo.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            vehiculos.append(vehiculo)    
                        
            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            vehiculo = EntradaVehiculo.objects.filter(fecha__date=start).count()
            vehiculos.append(vehiculo) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "vehiculos": vehiculos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_paquetes_dañados(request):    
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
    paquetes=[]
    danados=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            paquete = Paqueteria.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            paquetes.append(paquete)   

            danado =  Paqueteria.objects.filter(planta=objPlanta).filter(fecha__date=start).filter( Q(bolcables='1')  | Q(bolfaltainfo= '1') | Q(bolfuerahorario='1') | Q(bololor='1') | Q(bolpolvo='1') ).count()
            danados.append(danado)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            paquete = Paqueteria.objects.filter(fecha__date=start).count()
            paquetes.append(paquete) 

            danado = Paqueteria.objects.filter(fecha__date=start).filter( Q(bolcables='1')  | Q(bolfaltainfo= '1') | Q(bolfuerahorario='1') | Q(bololor='1') | Q(bolpolvo='1') ).count()
            danados.append(danado)
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "paquetes": paquetes,
    "danados": danados
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_materiales(request):    
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
    materiaprimas=[]
    quimicos=[]
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            materiaprima = ItemEntradaMaterial.objects.filter(planta=objPlanta).filter(entradamateriales_id__fecha__date=start).filter(tipo='materia prima').count()
            materiaprimas.append(materiaprima)   

            quimico =  ItemEntradaMaterial.objects.filter(planta=objPlanta).filter(entradamateriales_id__fecha__date=start).filter(tipo="quimico").count()
            quimicos.append(quimico)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            materiaprima = ItemEntradaMaterial.objects.filter(entradamateriales_id__fecha__date=start).filter(tipo='materia prima').count()
            materiaprimas.append(materiaprima) 

            quimico = ItemEntradaMaterial.objects.filter(entradamateriales_id__fecha__date=start).filter(tipo="quimico").count()
            quimicos.append(quimico)
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "materia prima": materiaprimas,
    "quimicos": quimicos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_areas_restingida(request):    
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
    entradas=[]
    
    
    
    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            entrada = Area_Restringida.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            entradas.append(entrada)   

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            entrada = Area_Restringida.objects.filter(fecha__date=start).count()
            entradas.append(entrada) 
            
            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "entradas": entradas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_empleado_sin_gafete(request):    
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
    vehiculares=[]
    personales=[]
    ambos=[]

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            vehicular = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetevehicular='1').filter(bolgafetepersonal='0').count()
            vehiculares.append(vehicular)

            personal = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='0').count()
            personales.append(personal)

            ambo = Empleado_Sin_Gafete.objects.filter(planta=objPlanta).filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='1').count()
            ambos.append(ambo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            vehicular = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetevehicular='1').filter(bolgafetepersonal='0').count()
            vehiculares.append(vehicular) 
            
            personal = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='0').count()
            personales.append(personal) 

            ambo = Empleado_Sin_Gafete.objects.filter(fecha__date=start).filter(bolgafetepersonal='1').filter(bolgafetevehicular='1').count()
            ambos.append(ambo) 

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "vehiculares": vehiculares,
    "personales": personales,
    "ambos": ambos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_entrada_equipo(request):    
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
    equipos=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            equipo = ItemEntradaEquipo.objects.filter(planta=objPlanta).filter(entradaequipo_id__fecha__date=start).count()
            equipos.append(equipo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            equipo = ItemEntradaEquipo.objects.filter(entradaequipo_id__fecha__date=start).count()
            equipos.append(equipo) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "equipos": equipos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_recibos(request):    
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
    recibos=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            recibo = RecibosAlmacen.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            recibos.append(recibo)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            recibo = RecibosAlmacen.objects.filter(fecha__date=start).count()
            recibos.append(recibo) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "recibos": recibos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_incidentes_servicio(request):    
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
    incidentes=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            incidente = Incidentes.objects.filter(planta=objPlanta).filter(fecha__date=start).count()
            incidentes.append(incidente)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            incidente = Incidentes.objects.filter(fecha__date=start).count()
            incidentes.append(incidente) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "incidentes": incidentes
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_rondines(request):    
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
    rondines=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            rondin = RondinHecho.objects.filter(planta=objPlanta).filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            rondines.append(rondin)

            dias.append(str(start.month) + "/" + str(start.day))                        
            start += delta        
    else:
        while start <= end:
            
            rondin = RondinHecho.objects.filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            rondines.append(rondin) 
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta        

    to_json = {
    "dias": dias,
    "rondines": rondines
    }
    
    return JsonResponse(to_json, safe=False)