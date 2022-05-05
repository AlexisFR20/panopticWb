

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
# importamos las vistas creadas en CORE
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

api_patterns = ([
    # Frontend Routes
    path('rondines', views.rondinList.as_view(), name='rondines'),
    path('rondin', views.api_load_rondin, name='rondin'),
    path('guardarrondinhecho', views.api_store_rondin_hecho, name='guardar_rondin_hecho'),
    path('iniciarrondin', views.api_start_rondin, name='iniciar_rondin'),
    path('agregarpunto', views.api_add_punto_hecho, name='add_punto_hecho'),
    path('finalizarrondin', views.api_finalizar_rondin, name='finalizar_rondin_hecho'),
    path('agregarevidencia', views.api_agregar_evidencia, name='agregar_evvidencia'),
    path('login', views.api_login, name='login'),
    path('logout', views.api_logout, name='logout'),
    path('cajones', views.api_get_patio, name="cajones"),
    path('markers', views.api_markers_list, name="mapacalor"), 
    #path('analytics', views.api_analytics_planta, name="analytics_planta"), 
    path('analytics',views.AnalyticsViews.as_view(),name="analytics_planta"),
    path('fvisitantes', views.api_fvisitantes, name="fvisitantes"),
    path('fvisitantes/lista', views.api_fvisitantes_list, name="fvisitantes_lista"),
    path('fvisitantes/salida', views.api_fvisitantes_salida, name="fvisitantes_salida"),
    path('festrilers', views.api_fes_trilers, name="festrilers"),
    path('festrilers/lista', views.api_fes_trilers_list, name="festrilers_lista"),
    path('festrilers/salida', views.api_fes_trilers_salida, name="festrilers_salida"),
    path('frevision18puntos', views.api_revision_18_puntos, name="frevision18puntos"),
    path('reportarincidente', views.api_reportar_incidente, name="reportar_incidente"),
    path('entradaequipo', views.api_entrada_equipo, name="entrada_equipo"),
    path('entradamateriales', views.api_entrada_materiales, name="entrada_materiales"),
    path('entradavehiculo', views.api_entrada_vehiculo, name="entrada_vehiculo"),
    path('entradaequipoget', views.api_entrada_equipo_get, name="entrada_equipo_get"),
    path('entradamaterialesget', views.api_entrada_material_get, name="entrada_materiales_get"),
    path('entradavehiculoget', views.api_entrada_vehiculo_get, name="entrada_vehiculo_get"),
    path('registropaqueteria', views.api_registro_paqueteria, name="registro_paqueteria"),
    path('empleadosingafete', views.api_empleado_singafete, name="empleado_singafete"),
    path('empleadosingafete/lista', views.api_empleado_singafete_list, name="empleado_singafete_lista"),
    path('empleadosingafete/salida', views.api_empleado_singafete_salida, name="empleado_singafete_salida"),
    path('arearestringida', views.api_acceso_area_restringida, name="area_restringida"),
    path('arearestringida/salida', views.api_acceso_area_restringida_salida, name="area_restringida_salida"),
    path('arearestringida/lista', views.api_acceso_area_restringida_list, name="area_restringida_lista"),
    path('recibosalmacen', views.api_recibos_almacen, name="recibos_almacen"),
    path('encuestas', views.api_load_encuestas, name="encuestas"),
    path('encuestas/contestar', views.api_new_encuesta_papeleta, name="encuestas_crear"),
    path('clientes', views.api_list_clientes, name="clientes_list"),
    path('updatetracking', views.api_update_tracking, name="update_tracking"),
    path('getgpstracking', views.api_gpstracking_get, name="get_tracking"),
    path('registernotificationtoken', views.api_register_notification_token, name='register_notification_token'),

    #Logistica/DD Management
    path('movimientos', views.api_list_movimientos, name="movimientos_lista"),
    path('movimientos/confirmarllegada', views.api_confirmar_llegada_movimiento, name="movimientos_confirmar_llegada"),
    path('movimientos/guardarticket', views.api_agregar_ticket, name="movimientos_guardar_ticket"),
    path('movimientos/reportarincidentevial', views.api_registrar_incidente_vial, name="movimientos_reporter_incidente_vial"),

    path('gps/list', views.get_gps_list, name="gps_list"),
    #CARTA PORTE
    path('traslados', views.get_traslados_list, name="cporte_list"),
    path('traslado', views.TrasladoId.as_view(), name="cporte_traslado"),

    #MEITRACK
    path('gps', views.gps_tracker, name="gps_tracker"),
], 'api')
