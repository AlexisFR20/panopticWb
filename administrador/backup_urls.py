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
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf.urls import (handler404)
# importamos las vistas creadas
from . import views

administrador_patterns = ([
    # Vistas de Administradorl
    path('', login_required(views.admin_home), name="admin_home"),   
    #  Sección Perfiles Global
    path('perfiles/global', login_required(views.admin_perfiles_global_index), name="admin_perfiles_global_index"),  
    path('perfiles/global/ver/<int:user_id>', login_required(views.admin_perfiles_global_show), name="admin_perfiles_global_show"),
    path('perfiles/global/editar/<int:user_id>', login_required(views.admin_perfiles_global_edit), name="admin_perfiles_global_edit"),     
    path('perfiles/global/crear', login_required(views.admin_perfiles_global_create), name="admin_perfiles_global_create"),     
    path('perfiles/global/remover/<int:user_id>', login_required(views.admin_perfiles_global_delete), name="admin_perfiles_global_delete"),     
    #  Sección Perfiles de Clientes
    path('perfiles/clientes', login_required(views.admin_perfiles_clientes_index), name="admin_perfiles_clientes_index"), 
    path('perfiles/clientes/ver/<int:user_id>', login_required(views.admin_perfiles_cliente_show), name="admin_perfiles_cliente_show"),
    path('perfiles/clientes/editar/<int:user_id>', login_required(views.admin_perfiles_cliente_edit), name="admin_perfiles_cliente_edit"),     
    path('perfiles/clientes/crear', login_required(views.admin_perfiles_cliente_create), name="admin_perfiles_cliente_create"),     
    path('perfiles/clientes/remover/<int:user_id>', login_required(views.admin_perfiles_cliente_delete), name="admin_perfiles_cliente_delete"),     
    #  Sección Perfiles de Personal
    path('perfiles/personal', login_required(views.admin_perfiles_personal_index), name="admin_perfiles_personal_index"), 
    path('perfiles/personal/ver/<int:user_id>', login_required(views.admin_perfiles_personal_show), name="admin_perfiles_personal_show"),
    path('perfiles/personal/editar/<int:user_id>', login_required(views.admin_perfiles_personal_edit), name="admin_perfiles_personal_edit"),     
    path('perfiles/personal/crear', login_required(views.admin_perfiles_personal_create), name="admin_perfiles_personal_create"),     
    path('perfiles/personal/remover/<int:user_id>', login_required(views.admin_perfiles_personal_delete), name="admin_perfiles_personal_delete"),     
    #  Sección de Unidades de Negocio
    path('unidades-de-negocio', login_required(views.admin_un_index), name="admin_un_index"), 
    path('unidades-de-negocio/editar/<int:un_id>', login_required(views.admin_un_edit), name="admin_un_edit"),   
    path('ajax/ajax_load_cinterno', views.ajax_load_cinterno, name="ajax_load_cinterno"),    
    #Sección de Sucursales
    path('sucursales', login_required(views.admin_sucursales_index), name = "admin_sucursales_index"),
    path('sucursales/crear', login_required(views.admin_sucursales_create), name="admin_sucursales_create"), 
    path('sucursales/editar/<int:suc_id>', login_required(views.admin_sucursales_edit), name = "admin_sucursales_edit"),
    # Rondines
    path('rondines/resumen', login_required(views.admin_rondines_resumen), name="admin_rondines_resumen"), 
    path('rondines/reportes', login_required(views.admin_rondines_reportes), name="admin_rondines_reportes"), 
    path('ajax/ajax_load_reporte_rondin', views.ajax_load_reporte_rondin, name="ajax_load_reporte_rondin"),
    path('ajax/ajax_load_reporte_puntos_hechos', views.ajax_load_reporte_puntos_hechos, name="ajax_load_reporte_puntos_hechos"),
    path('ajax/ajax_load_reporte_evidencias_de_puntos_hechos', views.ajax_load_reporte_evidencias_de_puntos_hechos, name="ajax_load_reporte_evidencias_de_puntos_hechos"),
    path('rondines/rondin/ver/<int:rondin_id>', login_required(views.admin_rondines_show), name="admin_rondines_show"), 
    path('rondines/rondin/crear', login_required(views.admin_rondines_rondin_create), name="admin_rondines_rondin_create"), 
    path('ajax/ajax_load_rondines_de_planta', views.ajax_load_rondines_de_planta, name="ajax_load_rondines_de_planta"),
    path('ajax/ajax_load_puntos_de_rondin', views.ajax_load_puntos_de_rondin, name="ajax_load_puntos_de_rondin"),
    path('ajax/ajax_desactivar_punto', views.ajax_desactivar_punto, name="ajax_desactivar_punto"),
    path('ajax/ajax_agregar_mod_punto', views.ajax_agregar_mod_punto, name="ajax_agregar_mod_punto"),
    path('ajax/ajax_load_tareas_de_rondin', views.ajax_load_tareas_de_rondin, name="ajax_load_tareas_de_rondin"),
    path('ajax/ajax_load_evidencias_de_rondin', views.ajax_load_evidencias_de_rondin, name="ajax_load_evidencias_de_rondin"),
    path('rondines/rondin/editar/<int:rondin_id>', login_required(views.admin_rondines_rondin_block_edit), name="admin_rondines_rondin_block_edit"), 
    path('ajax/ajax_load_rondin', views.ajax_load_rondin, name="ajax_load_rondin"),
    path('rondines/geocerca/<int:un_id>', login_required(views.admin_rondines_geocerca), name="admin_rondines_geocerca"), 
    path('rondines/geocerca/editar/<int:un_id>', login_required(views.admin_rondines_geocerca_edit), name="admin_rondines_geocerca_edit"), 
    path('rondines/mapa-interactivo', login_required(views.admin_rondines_mapa_interactivo), name="admin_rondines_mapa_interactivo"), 
    path('rondines/listado', login_required(views.admin_rondines), name="admin_rondines"), 
    path('rondines/impresion_qrs', login_required(views.admin_rondines_qr), name="admin_rondines_qr"), 
    path('rondines/estados-de-fuerza', login_required(views.admin_estados_fuerza), name="admin_estados_fuerza"), 
     #Movimiento
    path('movimientos/listado', login_required(views.admin_movimiento_listado), name="admin_movimiento_listado"), 
    path('movimientos/crear', login_required(views.admin_movimiento_create), name="admin_movimiento_create"), 
    path('movimientos/editar/<int:mov_id>', login_required(views.admin_movimiento_edit), name="admin_movimiento_edit"), 
    #Tipo Movimiento
    path('tipo-movimientos/listado', login_required(views.admin_tipo_movimiento_listado), name="admin_tipo_movimiento_listado"), 
    path('tipo-movimientos/crear', login_required(views.admin_tipo_movimiento_create), name="admin_tipo_movimiento_create"), 
    path('tipo-movimientos/editar/<int:tipo_mov_id>', login_required(views.admin_tipo_movimiento_edit), name="admin_tipo_movimiento_edit"),     
    #Proveedores
    path('proveedores/listado', login_required(views.admin_proveedores_listado), name="admin_proveedores_listado"), 
    path('proveedores/crear', login_required(views.admin_proveedores_create), name="admin_proveedores_create"), 
    path('proveedores/editar/<int:proveedor_id>', login_required(views.admin_proveedores_edit), name="admin_proveedores_edit"), 
    #Rangos 
    path('rangos-de-fecha', login_required(views.admin_rangos_fecha), name="admin_rangos_fecha"),
    #Predictive Analytics
    # Revisión 18 Puntos
    path('revision-18-puntos/historial', login_required(views.admin_18puntos_historial), name="admin_18puntos_historial"),
    path('revision-18-puntos/reportes', login_required(views.admin_18puntos_reportes), name = "admin_18puntos_reportes"),
    # Mapa Delictivo
    path('mapa-delictivo', login_required(views.admin_mapa_delictivo), name="admin_mapa_delictivo"),
    
    # E/S Trailers
    path('es-trailers/historial', login_required(views.admin_es_trailers_historial), name="admin_es_trailers_historial"),
    path('es-trailers/ver/<int:estra_id>', login_required(views.admin_es_trailers_ver), name="admin_es_trailers_ver"),    
    
    path('visitantes/lista', login_required(views.admin_visitantes), name="admin_viditantes_lista"),
    path('entradaequipo/lista', login_required(views.admin_entrada_equipo), name="admin_entradaequipo_lista"),
    path('incidentesservicio/lista', login_required(views.admin_incidentes_servicio), name="admin_incidentes_servicio_lista"),
    path('incidentesservicio/<int:id>', login_required(views.admin_incidentes_servicio_detalle), name="admin_incidentes_servicio_detalle"),
    
], 'administrador')   
