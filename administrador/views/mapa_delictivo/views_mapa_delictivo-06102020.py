from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from API.serializers import RondinSerializer
from entorno.models import Incidente, TipoIncidente
from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_18_puntos_Trailer, F_ES_Trailers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role, Notificacion
from core import user_validation
from django.http import HttpResponseRedirect, JsonResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.sites.models import Site  

from core import notifications
from core.externalModels import CiaaR1

import feedparser
import json

n = Notificacion.objects.filter(visto = False)

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

def admin_mapa_delictivo(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_maps_delictivo', 'js_moment', 'js_daterangepicker', 'js_datepicker']    
    
    incidentes = Incidente.objects.all()
    incidentes11 = Incidente.objects.order_by('-id').all()[0:9] #Barra izquierda
    plantas = Planta.objects.all()
    clientes = Cliente.objects.all()    
    notificaciones = n
    tipo_incidentes = TipoIncidente.objects.all()

    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente=cliente)

    return render(request, 'administrador/mapa_delictivo/index.html', { 'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'incidentes11': incidentes11, 'notificaciones': notificaciones, 'tipo_incidentes': tipo_incidentes } )
    
def admin_mapa_calor_incidentes(request):
    css_list = ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home']
    js_list = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js_mapa_calor', 'js_moment', 'js_daterangepicker', 'js_datepicker']    
    
    incidentes = Incidente.objects.all()    
    cliente = request.user.cliente
    plantas = Planta.objects.filter(cliente=cliente)
    clientes = Cliente.objects.all()
    notificaciones = n
    return render(request, 'administrador/zona0/mapas/mapa-calor.html', { 'css_list': css_list, 'js_list': js_list, 'incidentes': incidentes, 'plantas': plantas, 'clientes': clientes, 'notificaciones': notificaciones, 'cliente': cliente })


def parseRSS( rss_url ):
    return feedparser.parse( rss_url )

def getHeadlines(rss_url):
    headlines = []
    to_json = dict()
    json_object = []
    print(rss_url)
    feed = parseRSS(rss_url)
    
    for newsitem in feed['items']:

        """
        to_json += (
            ("title", newsitem['title']),
            ("link", newsitem['link']),
            ("description", newsitem['description']), 
            
        )
        
        #print(to_json)
        
        to_json += { 
            "title": newsitem['title'], 
            "link": newsitem['link'],
            "description": newsitem['description']
        }
        """

        to_json.update(
            {
                "noticia": {
                    "title": newsitem['title'],
                    "link": newsitem['link'],
                    "description": newsitem['description']
                }
            }
        )
        #print(to_json)
        #json_object += json.loads(to_json)
        #headlines.append(newsitem['title'])
        #headlines.append(newsitem['link'])
        #headlines.append(newsitem['description'])
        #headlines.append(newsitem['source'])
        #headlines.append(newsitem['source'].url)

    
    return to_json
    #return headlines
    #return list(to_json)
    #return JsonResponse(list(to_json), safe=False)

def news_rss(request):
    urlnews = "https://news.google.com/rss?hl=es-419&gl=MX&ceid=MX:es-419&limit=10"
    """
    allheadlines = []   

    newsurls = {

        'googlenews': urlnews,

    }

    #feedparser.parse(urlnews)[0].keys()
    for key, url in newsurls.items():
        
        #allheadlines.extend(getHeadlines(url))
        allheadlines += getHeadlines(url)


    #for hl in allheadlines:
    #    data += hl
    #    print(hl)
    #return {'xmldata': allheadlines}

    """
    headlines = []
    to_json = dict()
    json_object = []
    
    feed = parseRSS(urlnews)
    #print(list(feed))
    return JsonResponse(feed, safe=False)
    #return feed
    