from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.db.models import Avg
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse
from core.models import Planta, Cliente, User, Role
from arnes.models import *
from analytics.models import *
from API.serializers import *
from django.core import serializers
from django.db.models import Sum
from django.db.models import Q
from entorno.models import Incidente
from datetime import datetime
from django.utils import timezone
import datetime as dt
from functools import reduce
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
            entrada = F_ES_Trailers.objects.filter(planta=objPlanta.id).filter(entrada__date=start).count()
            entradas.append(entrada)    
                        
            salida = F_ES_Trailers.objects.filter(planta=objPlanta.id).filter(entrada__date=start).count()
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

            paquete = Paqueteria.objects.filter(un_id=objPlanta.id).filter(fecha__date=start).count()
            paquetes.append(paquete)   

            danado =  Paqueteria.objects.filter(un_id=objPlanta.id).filter(fecha__date=start).filter( Q(bolcables='1')  | Q(bolfaltainfo= '1') | Q(bolfuerahorario='1') | Q(bololor='1') | Q(bolpolvo='1') ).count()
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
            
            #equipo = ItemEntradaEquipo.objects.filter(planta=objPlanta).filter(entradaequipo_id__fecha__date=start).count()
            equipo = ItemEntradaEquipo.objects.filter(entradaequipo__planta_id=objPlanta.id).filter(entradaequipo_id__fecha__date=start).count()
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
    print("Planta:" + planta)
    #Dato de parámetros
    #cliente = Cliente.objects.filter(id=planta.cliente_id)
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
    
    auxrondines = Rondin.objects.filter(planta_id=planta.id)
    print("im am in")
    print(auxrondines)

    if planta:
    #if cliente:
        objPlanta = Planta.objects.get(pk=int(planta))
        #rondinesaux = Rondin.objects.filter(cliente_id=cliente.id)
        #rondineshechosaux = RondinHecho.objects.filter(reduce(lambda x, y: x | y, [Q(rondin_id=item.id) for item in rondinesaux]))
        #print("----------------------- Rondines: " + rondinesaux)
        #print("----------------------- Rondines Hechos: " + rondineshechosaux)
        while start <= end:
            
            #rondin = RondinHecho.objects.filter(planta=objPlanta).filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            rondin = RondinHecho.objects.filter(rondin__planta_id=objPlanta.id).filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
            #rondin = rondineshechosaux.filter(hora_inicio__date=start).filter(hora_fin__isnull=False).count()
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

def ajax_ceo_numero_rondines(request): 
    start = dt.date.today()
    lastmonth = start.replace(month = start.month - 1)

    planta = request.GET.get('planta_id')
    rondines = Rondin.objects.filter(planta_id=planta)
    rondineshechos = 0
    if rondines:
        rondineshechos = RondinHecho.objects.filter(reduce(lambda x, y: x | y, [Q(rondin_id=item.id) for item in rondines])).filter(hora_inicio__range=[lastmonth,start]).count()

    to_json = {
        "rondines": rondineshechos
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_ceo_recomendaciones(request):
    planta = request.GET.get('planta_id')
    papeletas = Papeleta.objects.filter(planta_id=planta)
    recomendaciones = None
    if papeletas:
        resultrec = Recomendacion.objects.filter(reduce(lambda x, y: x | y, [Q(papeleta_id=item.id) for item in papeletas])) 
        if resultrec:
            recomendaciones = serializers.serialize("json",resultrec)

    return HttpResponse(recomendaciones, content_type="application/json")

def ajax_ceo_numero_incidentes_rondines(request):
    planta = request.GET.get('planta_id')    
    incidentes = 0
    rondines = Rondin.objects.filter(planta_id=planta)
    rondineshechos = None
    start = dt.date.today()
    lastmonth = start.replace(month = start.month - 1)

    if rondines:
        rondineshechos = RondinHecho.objects.filter(reduce(lambda x, y: x | y, [Q(rondin_id=item.id) for item in rondines])).filter(hora_inicio__range=[lastmonth,start])
    
    if rondineshechos is not None:
        for p in rondineshechos:
            if EvidenciaPunto.objects.filter(rondinhecho_id = p.id).first() is not None:
                incidentes += 1
    
    to_json = {
        "incidentes": incidentes   
    }
    return JsonResponse(to_json, safe=False)

def ajax_ceo_personal_sin_gafete (request):    
    planta = request.GET.get('planta_id')
    ambos=[]               
    ambo = Empleado_Sin_Gafete.objects.filter(planta_id=planta).count()
    ambos.append(ambo) 

    to_json = {
    "ambos": ambos
    }
     
    return JsonResponse(to_json, safe=False)
    
def ajax_ceo_18_puntos(request):
    planta = request.GET.get('planta_id')
    puntos18 = F_18_puntos_Trailer.objects.filter(planta_id=planta).count()

    to_json = {
        "puntos": puntos18      
    }
    return JsonResponse(to_json, safe=False)

def ajax_num_visitantes (request):    
    planta = request.GET.get('planta_id')
    plantainst = Planta.objects.get(pk = planta)
    visitantes=0
    visitantes = F_Visitantes.objects.filter(planta=plantainst).count()
    
    to_json = {
    "visitantes": visitantes
    }
     
    return JsonResponse(to_json, safe=False)

def ajax_ponderacion (request):    
    ponderacion = 0
    
    planta_id = request.GET.get('planta_id')         
    
    planta = Planta.objects.get(pk=planta_id)
    
    ciudadPlanta = planta.ciudad
    
    ponderacion = list(Incidente.objects.filter(ciudad=ciudadPlanta).aggregate(Avg('nivel')).values())[0]
    
    to_json = {
        "ponderacion": ponderacion
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_capacitacion (request):    
    capacitaciones = []
    planta_id = request.GET.get('planta_id')  
    
    if planta_id!=None:        
        cliente = request.user.cliente
        planta =  Planta.objects.get(pk=planta_id)
        total = Concentracion.objects.filter(cliente=cliente).filter(sitio=planta).count()       
        pasados = Concentracion.objects.filter(cliente=cliente).filter(sitio=planta).filter(calificacion__gte = 7).count() 
    else:        
        cliente = request.user.cliente
        total = Concentracion.objects.filter(cliente=cliente).count()       
        pasados = Concentracion.objects.filter(cliente=cliente).filter(calificacion__gte = 7).count()     
    
    if total != 0:
        capacitacion = (pasados * 100)/total    
    else:
        capacitacion = 0   
    
    capacitaciones.append(capacitacion)
    
    
    to_json = {
        "capacitaciones": capacitaciones
    }
    
    return JsonResponse(to_json, safe=False)


def ajax_cobertura_planta (request):        
    turnos = 0   
    cubiertos = 0 
    cobertura = 0
    planta_id = request.GET.get('planta_id')      
    planta  = Planta.objects.get(pk=planta_id)

    if planta!=None:            
        estadosfuerza = EstadoFuerza.objects.filter(planta=planta).order_by("-fecha_inicio")       
        
        for ef in estadosfuerza:
            print('ef.total')
            print(ef.total())
            turnos = turnos + ef.total()
            if ef.cobertura_set.first():
                cubiertos = cubiertos + ef.cobertura_set.first().total()
        
        if turnos != 0:
            print('entrando al calculo')
            cobertura = round((cubiertos/turnos*100),2)
            
    else:
        cobertura = 0
        
    to_json = {
        "cobertura": cobertura
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_ceo_capacitacion (request):    
    
    capacitaciones = []

    total = Concentracion.objects.count()   
    pasados = Concentracion.objects.filter(calificacion__gte = 7).count() 
    capacitacion = (pasados * 100)/total
    capacitaciones.append(capacitacion)
    to_json = {
    "capacitaciones": capacitaciones
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_faltas(request):    
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
    faltas=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            falta = Falta.objects.filter(planta=objPlanta).filter(fecha=start).count()
            faltas.append(falta)

            dias.append(str(start.month) + "/" + str(start.day))
            start += delta
    else:
        while start <= end:
            
            falta = Falta.objects.filter(fecha=start).count()
            faltas.append(falta)
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta

    to_json = {
    "dias": dias,
    "faltas": faltas
    }
    
    return JsonResponse(to_json, safe=False)


def ajax_charts_numero_bajas(request):    
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
    bajas=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            baja = Baja.objects.filter(planta=objPlanta).filter(fecha=start).count()
            bajas.append(baja)

            dias.append(str(start.month) + "/" + str(start.day))
            start += delta
    else:
        while start <= end:
            
            baja = Baja.objects.filter(fecha=start).count()
            bajas.append(baja)
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta

    to_json = {
    "dias": dias,
    "bajas": bajas
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_vacantes(request):    
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
    vacantes=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            vacante = Vacante.objects.filter(planta=objPlanta).filter(fecha=start).count()
            vacantes.append(vacante)

            dias.append(str(start.month) + "/" + str(start.day))
            start += delta
    else:
        while start <= end:
            
            vacante = Vacante.objects.filter(fecha=start).count()
            vacantes.append(vacante)
             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta

    to_json = {
    "dias": dias,
    "vacantes": vacantes
    }
    
    return JsonResponse(to_json, safe=False)

def ajax_chart_cobertura(request):
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

    turnos = 0
    cubiertos = 0
    personas = 0
    bajas = 0
    rotacion=0

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))

        while start <= end:

            baja = Baja.objects.filter(planta=objPlanta).filter(fecha=start).count()
            bajas += baja
            efs = EstadoFuerza.objects.filter(planta=objPlanta).filter(fecha_inicio=start).all()
            print("efs "+str(efs.count()))
            for ef in efs:

                turnos += ef.total()
                personas += ef.personas()
                cubiertos += ef.cobertura_set.first().total()

            start += delta
    else:
        while start <= end:
            print("else")
            baja = Baja.objects.filter(fecha=start).count()
            bajas += baja
            efs = EstadoFuerza.objects.filter(fecha_inicio=start).all()
            print("efs "+str(efs.count()))
            for ef in efs:

                turnos += ef.total()
                personas += ef.personas()
                cubiertos += ef.cobertura_set.first().total()

            start += delta


    cobertura = 0
    if turnos>0:
        cobertura = (cubiertos/turnos)*100
    if personas>0:
        rotacion = (bajas/personas)*100

    to_json = {
        "cobertura": cobertura,
        "rotacion": rotacion,
    } 

    return JsonResponse(to_json, safe=False)

def ajax_charts_numero_capacitaciones(request):    
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
    capacitaciones=[]
    

    if planta:
        objPlanta = Planta.objects.get(pk=int(planta))
        
        while start <= end:

            capacitacion = Concentracion.objects.filter(sitio=objPlanta).filter(fecha_aplicacion__date=start).count()
            capacitaciones.append(capacitacion)

            dias.append(str(start.month) + "/" + str(start.day))
            start += delta
    else:
        while start <= end:
            
            capacitacion = Concentracion.objects.filter(fecha_aplicacion__date=start).count()
            capacitaciones.append(capacitacion)

             

            dias.append(str(start.month) + "/" + str(start.day))            
            start += delta

    to_json = {
        "dias": dias,
        "capacitaciones": capacitaciones
    }
    
    return JsonResponse(to_json, safe=False)
