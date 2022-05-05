from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse
from core.models import Planta, Cliente, User, Role, Notificacion
from ddmanagement.models import Movimiento, Vehiculo
from analytics.models import EstadoFuerza, Cobertura
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
import datetime as dt
import pytz

def ajax_get_per_cobertura(request):    
    planta_id = request.GET.get('planta_id')
    planta = Planta.objects.get(pk=planta_id)
    print(planta)
    estadoFuerza = EstadoFuerza.objects.filter(planta=planta).order_by('-id').first()
    cobertura = Cobertura.objects.get(estadofuerza=estadoFuerza)
    print(cobertura.porcentaje)
    to_json = {
        "cobertura_per": cobertura.porcentaje
    }
    
    return JsonResponse(to_json, safe=False) 