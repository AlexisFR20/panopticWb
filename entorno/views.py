from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Incidente, Alarma
from .tables import IncidenteTable, AlarmaTable
from django_tables2 import SingleTableView
from django_tables2 import RequestConfig
from django.urls import reverse, reverse_lazy
from . import charts
from .forms import IncidenteForm, AlarmaForm
from core.models import  Planta, Cliente, User, Role, Region, Sucursal, Ciudad
from core import user_validation
from entorno.models import Incidente, TipoIncidente

import datetime 
import json
from django.core import serializers
from django.db.models import Count
from django.db import connection

# Create your views here.
def zona0(request):
    #css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    #js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    #userdict = user_validation.validate(request)
    #user = User.objects.get(pk= userdict.get('user_id') ) 
    #incidentes = Incidente.objects.all()
    #incidentes11  = Incidente.objects.all()[0:11]
    #dash_context = request.session.get("django_plotly_dash", dict())
    #dash_context['userdict'] = userdict
    #**print("from view: "+str(userdict))
    #request.session['django_plotly_dash'] = dash_context
    #**print("from view: "+str(request.session['django_plotly_dash']))
    #return render(request, 'entorno/zona0.html', {"css_list": css_list, "js_list": js_list, 'userdict': userdict, 'user': user, 'incidentes': incidentes })
    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']

    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_clipboard', 'js_fancybox' ]
    cliente = request.user.cliente    
    #Borrado temporalmente mientras se checan permisos
    #if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
    #    plantas = Planta.objects.filter(cliente=cliente)
    #else:
    #    nombreplanta = request.user.planta       
    #    plantas = Planta.objects.filter(nombre=nombreplanta)  
    
    incidentes = Incidente.objects.all()  
    #plantas = Planta.objects.all()
    plantas = Planta.objects.filter(cliente=cliente)
    #clientes = Cliente.objects.all()
    tipo_incidentes = TipoIncidente.objects.all()  
    ciudades = Ciudad.objects.all()
    print("checkjuazz")
    print(tipo_incidentes) 
    #cliente = request.user.cliente

    #Este solo devuelve la planta a la que está ligado el usuario
    #plantas_v = Planta.objects.get(nombre=nombreplanta) 

    #se borro de return: 'vplantas': plantas_v

    return render(request, 'entorno/zona0.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'tipo_incidentes': tipo_incidentes, 'ciudades': ciudades, 'vcliente': cliente})

def incidentes_ajax(request):    
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

def zona0_per_type(request):
    

    css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin',  'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'fancybox']

    js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_clipboard', 'js_fancybox' ]
    
    cliente = request.user.cliente 

    tipo_incidente = request.GET.get('tipo_incidente')

    if request.user.role.alias_rol=='super': #si pertene a algún roles es altos privilegios según el cliente al que pertenece
        plantas = Planta.objects.filter(cliente=cliente)
    else:
        nombreplanta = request.user.planta       
        plantas = Planta.objects.filter(nombre=nombreplanta)  

    print(tipo_incidente)
    if tipo_incidente == None:
        incidentes = Incidente.objects.all()
    else:
        incidentes = Incidente.objects.filter(tipo=tipo_incidente)

    #plantas = Planta.objects.all()
    clientes = Cliente.objects.all()
    tipo_incidentes = TipoIncidente.objects.all()  
    ciudades = Ciudad.objects.all()  

    cliente = request.user.cliente
    plantas_v = Planta.objects.get(nombre=nombreplanta)
    
    return render(request, 'entorno/zona0_per_type.html', {'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'tipo_incidentes': tipo_incidentes, 'ciudades': ciudades, 'vcliente': cliente, 'vplantas': plantas_v, 'tipo_incidente': tipo_incidente })

def incidentes_per_type_ajax(request):    
    vciudad = request.GET.get('vciudad')
    vstart = request.GET.get('vstart')
    vend = request.GET.get('vend')
    vtipo_incidente = request.GET.get('vtipo_incidente')
    print("************")
    print(vciudad)
    print("************")
    print(vstart)
    print("************")
    print(vend)
    print("************")
    try:
        
        #go = list(Incidente.objects.values('tipo').annotate(dcount=Count('ciudad')).filter(fecha='2019-12-24') )
        if vciudad == None or vstart == None or vend == None or vtipo_incidente == None:     
            print("Sin")
            incidentes = Incidente.objects.all()

            incidentes = json.loads(serializers.serialize("json",incidentes))
           
            obj_incidentes = {
                "Res": 'OK',                
                "Incidente": incidentes
            }
        else:
            print("Con")
            incidentes = Incidente.objects.filter(fecha__range=(vstart, vend)).filter(tipo=vtipo_incidente) .all()
            
            incidentes = json.loads(serializers.serialize("json",incidentes))


            obj_incidentes = {
                "Res": 'OK',
                "Incidente": incidentes
            }

    except Incidente.DoesNotExist:
        go = None
        incidentes = None
        obj_incidentes = {
            "Res": 'ERROR',            
            
            "Incidente": incidentes
        }        
        #messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')

    return JsonResponse(obj_incidentes, safe=False)

def tipos_incidentes_get_ajax(request):        
    
    try:
        
        tipos_incidentes = TipoIncidente.objects.all()  

        tipos_incidentes = json.loads(serializers.serialize("json",tipos_incidentes))
           
        obj_incidentes = {
            "res": 'OK',                
            "tipos_incidentes": tipos_incidentes
        }
        

    except Incidente.DoesNotExist:
        go = None
        incidentes = None
        obj_incidentes = {
            "res": 'ERROR',            
            "tipos_incidentes": '0'
        }        
        #messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')

    return JsonResponse(obj_incidentes, safe=False)

def principal(request):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    chart_div = charts.chart_histograma_delitos()
        
    userdict = user_validation.validate(request) 
    user = User.objects.get(pk= userdict.get('user_id') )    
    return render(request, 'entorno/principal.html', {'chart_div': chart_div, "css_list": css_list, "js_list": js_list, 'userdict': userdict, 'user': user})

class IncidenteCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    model = Incidente
    form_class = IncidenteForm    
    
    def get_success_url(self):
        return reverse('entorno:list')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.user = self.request.user
        
        form.save()
        return super().form_valid(form)
    
    

class IncidenteUpdate(UpdateView):
    model = Incidente
    fields = ["tipo", "cantidad", "fecha", "direccion", "ciudad", "estado", "pais", "lat", "lng", "url_noticia"]
    template_name = 'entorno/incidente_update_form.html'

    def get_success_url(self):
        return reverse_lazy('entorno:update', args=[self.object.id]) + '?ok'

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class IncidenteDelete(DeleteView):
    model = Incidente
    success_url = reverse_lazy('lista_incidente')

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context


    

class IncidenteListView(SingleTableView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    table_class = IncidenteTable
    template_name = 'entorno/list_incidentes.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Incidente.objects.filter(tipo__contains=query)
        else:
            lista = Incidente.objects.all()
        return lista
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context
        
class AlarmaCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    model = Alarma
    form_class = AlarmaForm    
    
    def get_success_url(self):
        #modulo:ruta
        return reverse('entorno:alarma_list')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the alarms        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class AlarmaListView(SingleTableView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    table_class = AlarmaTable
    template_name = 'entorno/list_alarmas.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Alarma.objects.filter(tipo__contains=query)
        else:
            lista = Alarma.objects.all()
        return lista
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context
