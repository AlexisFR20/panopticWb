"""panoptic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# importamos las vistas creadas en CORE
from . import views

analytics_patterns = ([
    # Frontend Routes
    #path('', views.home, name='home'),
    #Dashboard Predictive Analytics
    #path('', views.predictive_analytics_dashboard, name="home"),
    path('', views.home, name="home"),
    path('<int:id>', views.home_planta, name='home_planta'),
    path('rondines/dashboard', views.rondines_dashboard, name="rondines_dashboard"),
    path('rondines/rondinhecho/<int:id>', views.rondinhecho, name="rondinhecho_detalle"),
    path('visitantes/dashboard', views.fvisitantes_dashboard, name="visitantes_dashboard"),
    path('visitantes/<int:pk>/detalles', views.fvisitantes_detail, name="fvisitantes_detail"),

    path('empleadossingafete/dashboard', views.empleadossingafete_dashboard, name="empleadossingafete_dashboard"),
    path('arearestringida/dashboard', views.arearestringida_dashboard, name="arearestringida_dashboard"),
    path('recibos/dashboard', views.recibos_dashboard, name="recibos_dashboard"),
    #path('recibo-almacen/dashboard', views.recibo_almacen_dashboard, name="recibo_almacen_dashboard"),
    path('recibos/<int:pk>/detalles', views.recibos_detail, name="recibos_detail"),

    path('paqueteria/dashboard', views.paqueteria_dashboard, name="paqueteria_dashboard"),
    path('paqueteria/<int:pk>/detalles', views.paqueteria_detail, name="paqueteria_detail"),
    path('rondines', views.RondinesList.as_view(), name='list_rondines'),
    path('rondines/crear', views.RondinCreate.as_view(), name='create_rondin'),
    path('rondines/<int:pk>/editar', views.RondinUpdate.as_view(), name='update_rondin'),
    path('rondines/<int:pk>/detalles', views.RondinDetail.as_view(), name='detail_rondin'),
    path('rondines/<int:pk>/eliminar', views.RondinDelete.as_view(), name='delete_rondin'),
    path('rondines/<int:pk>/punto/crear', views.PuntoCreate.as_view(), name='create_punto'),
    path('rondines/punto/<int:pk>/editar', views.PuntoUpdate.as_view(), name='update_punto'),
    #path('visitantes', views.RondinesList.as_view(), name='list_rondines'),
    path('ajax/load_plantas_options', views.ajax_load_plantas, name="ajax_load_plantas_options"),

    path('estados-de-fuerza', views.estados_fuerza, name="estados_fuerza"),
    path('estados-de-fuerza/ajax', views.ajax_load_estados_fuerza, name="estados_fuerza_ajax"), 
    path('faltas/lista', views.falta_list, name="falta_list"), 
    path('bajas/lista', views.baja_list, name="baja_list"), 
    path('vacantes/lista', views.vacante_list, name="vacante_list"),

    path('es-trailers/dashboard', views.es_trailers_dashboard, name="es_trailers_dashboard"), 
    path('es-trailers/<int:pk>/detalles', views.es_trailers_detail, name="es_trailers_detail"),

    path('logros/dashboard', views.logros_dashboard, name="logros_dashboard"), 
    path('logros/<int:pk>/detalles', views.logros_detail, name="logros_detail"),
], 'analytics')
