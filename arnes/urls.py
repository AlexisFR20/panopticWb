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

arnes_patterns = ([
    # Frontend Routes
    path('', views.home, name='home'),
    path('<int:id>', views.home_planta, name='home_planta'),
    path('encuestas/', views.encuestas.as_view(), name="list_encuestas"),
    path('encuestas/crear', views.EncuestaCreate.as_view(), name="create_encuesta"),
    path('encuestas/detalles/<int:pk>', views.EncuestaDetail.as_view(), name="detail_encuesta"),
    path('encuestas/detalles/<int:pk>/pregunta/crear', views.PreguntaCretae.as_view(), name="create_pregunta"),
    path('encuestas/editar/<int:pk>', views.EncuestaUpdate.as_view(), name="update_encuesta"),
    path('encuestas/eliminar/<int:pk>', views.EncuestaDelete.as_view(), name="delete_encuesta"),
    path('encuestas/categorias/crear', views.CategoriaEncuestaCreate.as_view(), name="create_categoria"),
    path('encuestas/<int:pk>/papeletas/crear', views.PapeletaCreate.as_view(), name="create_papeleta"), 
    path('encuestas/papeletas/detalles/<int:pk>', views.PapeletaDetail.as_view(), name="detail_papeleta"),
    path('encuestas/papeletas/lista', views.papeletas, name="list_papeletas"),
    path('encuestas/roadmap', views.roadmap, name="roadmap"),
    path('encuestas/roadmap/ajax-tabla', views.ajax_roadmap_tabla, name="ajax_roadmap_tabla"),
    path('encuestas/resultados-analisis-riesgo', views.resultados_analisis_riesgo, name="resultados_analisis_riesgo"),
], 'arnes')
