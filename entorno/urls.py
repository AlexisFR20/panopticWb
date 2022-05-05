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
#from django.contrib import admin
from django.urls import path
# importamos las vistas creadas en CORE
from . import views

entorno_patterns = ([
    # Frontend Routes
    path('', views.principal, name='dashboard'),
    path('incidentes/crear/', views.IncidenteCreate.as_view(), name="create"),
    path('incidentes/', views.IncidenteListView.as_view(), name="list"),
    path('incidentes/editar/<int:pk>/', views.IncidenteUpdate.as_view(), name="update"),
    path('incidentes/eliminar/<int:pk>/', views.IncidenteDelete.as_view(), name="delete"),
    path('zona0/', views.zona0, name="zona0"),
    path('zona0/incidentes_ajax', views.incidentes_ajax, name="incidentes_ajax"),

    path('zona0/tipo-de-incidente', views.zona0_per_type, name="zona0_per_type"),
    path('zona0/incidentes_per_type_ajax', views.incidentes_per_type_ajax, name="incidentes_per_type_ajax"),

    path('tipos_incidentes_get_ajax', views.tipos_incidentes_get_ajax, name="tipos_incidentes_get_ajax"),
    
    path('alarmas/crear/', views.AlarmaCreate.as_view(), name="alarma_create"),
    path('alarmas/', views.AlarmaListView.as_view(), name="alarma_list"),
], 'entorno')
