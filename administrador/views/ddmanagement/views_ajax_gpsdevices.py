from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from django.http import JsonResponse, HttpResponse
from core.models import Planta, Cliente, User, Role
from ddmanagement.models import gpsdevice
from django.core import serializers
from django.db.models import Sum
from datetime import datetime
from django.utils import timezone
import datetime as dt
import pytz

# Vistas de movimientos en Dashboard de Administrador
def ajax_lista_gpsdevices(request):    
    cliente = request.GET.get('cliente') #id    
    dataset = gpsdevice.objects.filter(asignado=True).all()    
    data=serializers.serialize ("json", dataset, use_natural_foreign_keys=False)    
    return JsonResponse(data, safe=False) 