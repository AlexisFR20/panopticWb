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
from arnes import urls
from administrador.views.predictive_analytics.views_paqueteria import *
from administrador.views.predictive_analytics.views_empleadosg  import *
from administrador.views.predictive_analytics.views_area import *
from administrador.views.ddmanagement.views_chofer import *
from administrador.views.ddmanagement.views_vehiculo import *
from administrador.views.ddmanagement.views_gpsdevices import *
from core.views.roles.views_roles import *
from administrador.views.areas_permisos.views_areas_permisos import *
from administrador.views.permisos.views_permisos import *
from administrador.views.predictive_analytics.views_visitantes_new import *
from .views import generate_pdf_analisis_riesgo, generate_pdf_predictive

administrador_patterns = ([
    #Vistas de Cuentas    
    path('cuentas/principal', login_required(views.CuentasPrincipal), name = "cuentas_principal"),    
    path('cuentas/permisos-por-tipo-usuario', login_required(views.CuentasPermisosPorTipo), name = "cuentas_permisos_tipo"),   
    #Areas permisos   
    path('cuentas/areas-de-permisos/crear', login_required(AreapermisoCreateView.as_view()), name="areas_permisos_create"),
    path('cuentas/areas-de-permisos/listado', login_required(AreapermisoListView.as_view()), name="areas_permisos_list"),
    path('cuentas/areas-de-permisos/<int:pk>', login_required(AreapermisoDetailView.as_view()), name='areas_permisos_detailview'),
    path('cuentas/areas-de-permisos/editar/<int:pk>/', login_required(AreapermisoUpdateView.as_view()), name="areas_permisos_update"),
    path('cuentas/areas-de-permisos/borrar/<int:pk>/', login_required(AreapermisoDeleteView.as_view()), name="areas_permisos_delete"),       
    #Vistas de Permisos
    path('cuentas/permisos/crear', login_required(PermisosCreateView.as_view()), name="permisos_create"),
    path('cuentas/permisos/listado', login_required(PermisosListView.as_view()), name="permisos_list"),
    path('cuentas/permisos/<int:pk>', login_required(PermisosDetailView.as_view()), name='permisos_detailview'),
    path('cuentas/permisos/editar/<int:pk>/', login_required(PermisosUpdateView.as_view()), name="permisos_update"),
    path('cuentas/permisos/borrar/<int:pk>/', login_required(PermisosDeleteView.as_view()), name="permisos_delete"),          
    # Vistas de Administradorl
    path('', login_required(views.admin_home), name="admin_home"),   
    #  Sección Perfiles Global
    path('perfiles/global', login_required(views.admin_perfiles_global_index), name="admin_perfiles_global_index"),  
    path('perfiles/global/ver/<int:user_id>', login_required(views.admin_perfiles_global_show), name="admin_perfiles_global_show"),
    path('perfiles/global/editar/<int:user_id>', login_required(views.admin_perfiles_global_edit), name="admin_perfiles_global_edit"),     
    path('perfiles/global/crear', login_required(views.admin_perfiles_global_create), name="admin_perfiles_global_create"),     
    path('perfiles/global/remover/<int:user_id>', login_required(views.admin_perfiles_global_delete), name="admin_perfiles_global_delete"),     
    #  Sección Perfiles de Clientes
    #path('perfiles/clientes', login_required(views.admin_perfiles_clientes_index), name="admin_perfiles_clientes_index"), 
    #path('perfiles/clientes/ver/<int:user_id>', login_required(views.admin_perfiles_cliente_show), name="admin_perfiles_cliente_show"),
    #path('perfiles/clientes/editar/<int:user_id>', login_required(views.admin_perfiles_cliente_edit), name="admin_perfiles_cliente_edit"),     
    #path('perfiles/clientes/crear', login_required(views.admin_perfiles_cliente_create), name="admin_perfiles_cliente_create"),     
    #path('perfiles/clientes/remover/<int:user_id>', login_required(views.admin_perfiles_cliente_delete), name="admin_perfiles_cliente_delete"),     
    path('perfiles/clientes/crear', login_required(views.ClienteCreateView.as_view()), name="cliente_create"),
    path('perfiles/clientes', login_required(views.ClienteListView.as_view()), name="cliente_list"),
    path('perfiles/clientes/ver/<int:pk>', login_required(views.ClienteDetailView.as_view()), name='cliente_detailview'),
    path('perfiles/clientes/editar/<int:pk>', login_required(views.ClienteUpdateView.as_view()), name="cliente_update"),
    path('perfiles/clientes/remover/<int:pk>/', login_required(views.ClienteDelete.as_view()), name="cliente_delete"),

    #CartaPorte
    path('cartaporte/clientes/crear', login_required(views.PorteClienteCreateView.as_view()), name="porte_cliente_create"),
    #path('cartaporte/productos/crear', login_required(views.porteProducto), name="porte_producto_create"),
    #path('cartaporte/productos/remover/<str:id>', login_required(views.porteProductoDelete), name="porte_producto_delete"),
    #path('cartaporte/productos/editar/<str:id>', login_required(views.porteProductoUpdate), name="porte_producto_update"),
    #path('cartaporte/productos', login_required(views.porteProductoList), name="porte_producto_list"),
    #path('cartaporte/receiver/crear', login_required(views.PorteReceiverCreateView.as_view()), name="porte_receiver_create"),
    #path('cartaporte/receiver/remover/<int:id>', login_required(views.porteReceiverDelete), name="porte_receiver_delete"),
    #path('cartaporte/receiver/editar/<int:pk>', login_required(views.PorteReceiverUpdate.as_view()), name="porte_receiver_update"),
    #path('cartaporte/receiver', login_required(views.porteReceiverList), name="porte_receiver_list"),
    #path('cartaporte/facturas/crear',login_required(views.porteFactura), name="porte_factura_create"),
    #path('cartaporte/facturas',login_required(views.porteFacturaList), name="porte_factura_list"),
    #path('cartaporte/codigopostal',login_required(views.getPostalCode),name="get_cp"),
    #path('cartaporte/codigounidades', login_required(views.getProductoServicioCode),name="get_unidades"),
    #path('cartaporte/claveproducto',login_required(views.getClaveProducto),name="get_clave"),
    #path('cartaporte/ubicacion', login_required(views.getUbicacion),name="get_ubicacion"),
    #  Sección Perfiles de Personal
    path('perfiles/personal', login_required(views.admin_perfiles_personal_index), name="admin_perfiles_personal_index"), 
    path('perfiles/personal/ver/<int:user_id>', login_required(views.admin_perfiles_personal_show), name="admin_perfiles_personal_show"),
    path('perfiles/personal/editar/<int:user_id>', login_required(views.admin_perfiles_personal_edit), name="admin_perfiles_personal_edit"),     
    path('perfiles/personal/crear', login_required(views.admin_perfiles_personal_create), name="admin_perfiles_personal_create"),     
    path('perfiles/personal/remover/<int:user_id>', login_required(views.admin_perfiles_personal_delete), name="admin_perfiles_personal_delete"),     
    #  Sección de Unidades de Negocio
    path('unidades-de-negocio', login_required(views.admin_un_index), name="admin_un_index"), 
    path('unidades-de-negocio/editar/<int:un_id>', login_required(views.admin_un_edit), name="admin_un_edit"),   
    path('unidades-de-negocio/remover/<int:un_id>', login_required(views.admin_un_delete), name="admin_un_delete"),    
    path('ajax/ajax_load_cinterno', views.ajax_load_cinterno, name="ajax_load_cinterno"),    
    #Sección de Sucursales
    path('sucursales', login_required(views.admin_sucursales_index), name = "admin_sucursales_index"),
    path('sucursales/crear', login_required(views.admin_sucursales_create), name="admin_sucursales_create"), 
    path('sucursales/editar/<int:suc_id>', login_required(views.admin_sucursales_edit), name = "admin_sucursales_edit"),
    path('sucursales/remover/<int:suc_id>', login_required(views.admin_sucursales_delete), name = "admin_sucursales_delete"),
    #Sección de Regiones
    path('regiones', login_required(views.admin_regiones_index), name = "admin_regiones_index"),
    path('regiones/crear', login_required(views.admin_regiones_create), name="admin_regiones_create"), 
    path('regiones/editar/<int:reg_id>', login_required(views.admin_regiones_edit), name = "admin_regiones_edit"),
    path('regiones/remover/<int:reg_id>', login_required(views.admin_regiones_delete), name = "admin_regiones_delete"),
    #Roles
    path('rol/crear',RoleCreateView.as_view(), name="role_create"),
    path('rol/lista', RoleListView.as_view(), name="role_list"),
    path('rol/<int:pk>', RoleDetailView.as_view(), name='role_detailview'),
    path('rol/editar/<int:pk>/', RoleUpdateView.as_view(), name="role_update"),
    path('rol/borrar/<int:pk>/', RoleDelete.as_view(), name="role_delete"), 
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
    path('estados-de-fuerza', login_required(views.admin_estados_fuerza), name="admin_estados_fuerza"), 
    path('estados-de-fuerza/<int:id>/edit', login_required(views.admin_estados_fuerza_edit), name="admin_estados_fuerza_edit"),
    path('estados-de-fuerza/<int:pk>/delete', login_required(views.EstadoFuerzaDelete.as_view()), name="admin_estados_fuerza_delete"),
    path('estados-de-fuerza/<int:id>/cobertura', login_required(views.admin_estados_fuerza_cobertura_create), name="admin_estados_fuerza_cobertura_create"), 
    path('estados-de-fuerza/crear', login_required(views.admin_estados_fuerza_create), name="admin_estados_fuerza_create"), 
    path('estados-de-fuerza/ajax', login_required(views.ajax_load_estados_fuerza), name="admin_estados_fuerza_ajax"), 
    path('estados-de-fuerza/get/cobertura', login_required(views.load_estados_fuerza_by_range), name="load_estados_fuerza_by_range"), 
    path('faltas/crear', login_required(views.admin_falta_create.as_view()), name="admin_falta_create"),
    path('faltas/lista', login_required(views.admin_falta_list), name="admin_falta_list"),
    path('faltas/<int:id>/editar', login_required(views.admin_falta_edit), name="admin_falta_edit"),
    path('faltas/<int:pk>/borrar', login_required(views.FaltaDelete.as_view()), name="admin_falta_delete"),
    path('bajas/crear', login_required(views.admin_baja_create), name="admin_baja_create"),
    path('bajas/<int:id>/editar', login_required(views.admin_baja_edit), name="admin_baja_edit"),
    path('bajas/lista', login_required(views.admin_bajas_list), name="admin_baja_list"),
    path('bajas/<int:pk>/borrar', login_required(views.BajaDelete.as_view()), name="admin_baja_delete"),
    path('vacantes/lista', login_required(views.admin_vacantes_list), name="admin_vacante_list"),
    path('vacantes/crear', login_required(views.admin_vacante_create), name="admin_vacante_create"),
    path('vacantes/<int:id>/editar', login_required(views.admin_vacante_edit), name="admin_vacante_edit"),
    path('vacantes/<int:pk>/borrar', login_required(views.VacanteDelete.as_view()), name="admin_vacante_delete"),
    path('asistencias', login_required(views.admin_asistencias), name="admin_asistencias"),
     #Movimiento
    #path('movimientos/listado', login_required(views.admin_movimiento_listado), name="admin_movimiento_listado"), 
    #path('movimientos/crear', login_required(views.admin_movimiento_create), name="admin_movimiento_create"), 
    #path('movimientos/editar/<int:mov_id>', login_required(views.admin_movimiento_edit), name="admin_movimiento_edit"), 
    #Tipo Movimiento
    path('tipo-movimientos/mapa-de-movimientos', login_required(views.admin_mapa_movimientos), name="admin_mapa_movimientos"), 
    path('tipo-movimientos/mapa-movimientos', login_required(views.mapa_movimientos), name="mapa_movimientos"), 
    path('tipo-movimientos/listado', login_required(views.admin_tipo_movimiento_listado), name="admin_tipo_movimiento_listado"), 
    path('tipo-movimientos/crear', login_required(views.admin_tipo_movimiento_create), name="admin_tipo_movimiento_create"), 
    path('tipo-movimientos/editar/<int:tipo_mov_id>', login_required(views.admin_tipo_movimiento_edit), name="admin_tipo_movimiento_edit"),     
    
    #Rangos 
    path('rangos-de-fecha', login_required(views.admin_rangos_fecha), name="admin_rangos_fecha"),
    #Seccion de Predictive Analytics /////////////////////////////////////////////////////////////////////////////////////////////////////
    path('ajax/get/entradas_salidas_trailers', login_required(views.ajax_charts_numero_entradas_salidas_trailers), name= "get_ajax_charts_numero_entradas_salidas_trailers"), 
    path('ajax/get/revision_18_puntos', login_required(views.ajax_charts_revision_18_puntos), name="get_ajax_charts_revision_18_puntos"),
    path('ajax/get/numero_registro_visitantes', login_required(views.ajax_charts_numero_registro_visitantes), name="get_ajax_charts_numero_registro_visitantes"),
    path('ajax/get/numero_registro_vehiculos', login_required(views.ajax_charts_numero_registro_vehiculos), name="get_ajax_charts_numero_registro_vehiculos"),
    path('ajax/get/numero_incidentes_servicio', login_required(views.ajax_charts_numero_incidentes_servicio), name= "get_ajax_charts_numero_incidentes_servicio"), 
    path('ajax/get/numero_paquetes_dañados', login_required(views.ajax_charts_numero_paquetes_dañados), name="get_ajax_charts_numero_paquetes_dañados"),
    path('ajax/get/numero_entrada_materiales', login_required(views.ajax_charts_numero_entrada_materiales), name="get_ajax_charts_numero_entrada_materiales"),
    path('ajax/get/numero_entrada_areas_restingida', login_required(views.ajax_charts_numero_entrada_areas_restingida), name="get_ajax_charts_numero_entrada_areas_restingida"),
    path('ajax/get/numero_empleado_sin_gafete', login_required(views.ajax_charts_numero_empleado_sin_gafete), name="get_ajax_charts_numero_empleado_sin_gafete"),
    path('ajax/get/numero_entrada_equipo', login_required(views.ajax_charts_numero_entrada_equipo), name="get_ajax_charts_numero_entrada_equipo"),
    path('ajax/get/numero_recibos', login_required(views.ajax_charts_numero_recibos), name="get_ajax_charts_numero_recibos"),
    path('ajax/get/numero_rondines', login_required(views.ajax_charts_numero_rondines), name="get_ajax_charts_numero_rondines"),

    path('ajax/get/numero_faltas', login_required(views.ajax_charts_numero_faltas), name="get_ajax_charts_numero_faltas"),
    path('ajax/get/numero_bajas', login_required(views.ajax_charts_numero_bajas), name="get_ajax_charts_numero_bajas"),
    path('ajax/get/numero_vacantes', login_required(views.ajax_charts_numero_vacantes), name="get_ajax_charts_numero_vacantes"),
    path('ajax/get/cobertura', login_required(views.ajax_chart_cobertura), name="get_ajax_chart_cobertura"),
    path('ajax/get/numero_capacitaciones', login_required(views.ajax_charts_numero_capacitaciones), name="get_ajax_chart_numero_capacitaciones"),

    #Dashboard Predictive Analytics    
    path('dashboard-predictive-analytics', login_required(views.admin_predictive_analytics_dashboard), name="admin_predictive_analytics_dashboard"),
    #Formato de E/S Trailers
    path('es-trailers/historial', login_required(views.admin_es_trailers_historial), name="admin_es_trailers_historial"),
    path('es-trailers/ver/<int:estra_id>', login_required(views.admin_es_trailers_ver), name="admin_es_trailers_ver"),     
    #Formato de Revision 18 Puntos
    path('revision-18-puntos/historial', login_required(views.admin_18puntos_historial), name = "admin_18puntos_historial"),
    path('revision-18-puntos/historial/ver/<int:rev_id>', login_required(views.admin_18puntos_historial_show), name="admin_18puntos_historial_show"),    
    path('ajax/ajax_load_reporte_18puntos', views.ajax_load_reporte_18puntos, name="ajax_load_reporte_18puntos"),
    path('revision-18-puntos/reportes', login_required(views.admin_18puntos_reportes), name = "admin_18puntos_reportes"),
    #Formato Paqueteria
    path('paqueteria/crear', PaqueteriaCreateView.as_view(), name="paqueteria_create"),
    path('paqueteria/historial', PaqueteriaListView.as_view(), name="paqueteria_list"),
    path('paqueteria/<int:pk>', PaqueteriaDetailView.as_view(), name='paqueteria_detailview'),
    path('paqueteria/editar/<int:pk>/', PaqueteriaUpdateView.as_view(), name="paqueteria_update"),
    path('paqueteria/borrar/<int:pk>/', PaqueteriaDelete.as_view(), name="paqueteria_delete"),
    #Formato Empleados Sin gafete
    path('empleado-sin-gafete/crear', EmpleadosgCreateView.as_view(), name="empleadosg_create"),
    path('empleado-sin-gafete/historial', EmpleadosgListView.as_view(), name="empleadosg_list"),
    path('empleado-sin-gafete/<int:pk>', EmpleadosgDetailView.as_view(), name='empleadosg_detailview'),
    path('empleado-sin-gafete/editar/<int:pk>/', EmpleadosgUpdateView.as_view(), name="empleadosg_update"),
    path('empleado-sin-gafete/borrar/<int:pk>/', EmpleadosgDelete.as_view(), name="empleadosg_delete"),
    #Formato area Restringida
    path('area-restringida/crear', AreaCreateView.as_view(), name="area_create"),
    path('area-restringida/historial', AreaListView.as_view(), name="area_list"),
    path('area-restringida/<int:pk>', AreaDetailView.as_view(), name='area_detailview'), 
    path('area-restringida/editar/<int:pk>/', AreaUpdateView.as_view(), name="area_update"),
    path('area-restringida/borrar/<int:pk>/', AreaDelete.as_view(), name="area_delete"),
    
    #Formato de Empleados sin Gafete
    path('empleados-sin-gafete/lista', login_required(views.admin_empleados_sin_gafete), name="admin_empleados_sin_gafete_lista"),
    path('empleados-sin-gafete/registrar', login_required(views.admin_empleados_sin_gafete_registrar), name="admin_empleados_sin_gafete_registrar"),
    #Fromato de  Entrada de Servicio
    path('entradaequipo/lista', login_required(views.admin_entrada_equipo), name="admin_entradaequipo_lista"),
    path('incidentes-de-servicio/lista', login_required(views.admin_incidentes_servicio), name = "admin_incidentes_servicio_lista"),
    path('incidentes-de-servicio/<int:id>', login_required(views.admin_incidentes_servicio_detalle), name="admin_incidentes_servicio_detalle"),
    # Seccion de Capacitacion
    #Categoria Curso
    path('categoria-curso/crear', login_required(views.CategoriaCursoCreateView.as_view()), name="categoria_curso_create"),
    path('categoria-curso/historial', login_required(views.CategoriaCursoListView.as_view()), name="categoria_curso_list"),
    path('categoria-curso/<int:pk>', login_required(views.CategoriaCursoDetailView.as_view()), name='categoria_curso_detailview'),
    path('categoria-curso/editar/<int:pk>/', login_required(views.CategoriaCursoUpdateView.as_view()), name="categoria_curso_update"),
    path('categoria-curso/borrar/<int:pk>/', login_required(views.CategoriaCursoDelete.as_view()), name="categoria_curso_delete"),
    #Grado
    path('grado/crear', login_required(views.GradoCreateView.as_view()), name="grado_create"),
    path('grado/historial', login_required(views.GradoListView.as_view()), name="grado_list"),
    path('grado/<int:pk>', login_required(views.GradoDetailView.as_view()), name='grado_detailview'),
    path('grado/editar/<int:pk>/', login_required(views.GradoUpdateView.as_view()), name="grado_update"),
    path('grado/borrar/<int:pk>/', login_required(views.GradoDelete.as_view()), name="grado_delete"), 
    #Curso
    path('curso/crear', login_required(views.CursoCreateView.as_view()), name="curso_create"),
    path('curso/historial', login_required(views.CursoListView.as_view()), name="curso_list"),
    path('curso/<int:pk>', login_required(views.CursoDetailView.as_view()), name='curso_detailview'),
    path('curso/editar/<int:pk>/', login_required(views.CursoUpdateView.as_view()), name="curso_update"),
    path('curso/borrar/<int:pk>/', login_required(views.CursoDelete.as_view()), name="curso_delete"),
    #Gestion de Concentracion
    path('concentracion/crear', login_required(views.ConcentracionCreateView.as_view()), name="concentracion_create"),
    path('concentracion/historial', login_required(views.ConcentracionListView.as_view()), name="concentracion_list"),
    path('concentracion/<int:pk>', login_required(views.ConcentracionDetailView.as_view()), name='concentracion_detailview'),
    path('concentracion/editar/<int:pk>/', login_required(views.ConcentracionUpdateView.as_view()), name="concentracion_update"),
    path('concentracion/borrar/<int:pk>/', login_required(views.ConcentracionDelete.as_view()), name="concentracion_delete"),     
    # Mapa Delictivo y de Calor de Incidentes
    path('mapa-delictivo', login_required(views.admin_mapa_delictivo), name="admin_mapa_delictivo"),
    path('mapa-de-calor', login_required(views.admin_mapa_calor_incidentes), name="admin_mapa_calor_incidentes"),
    path('ciudades', login_required(views.admin_agregar_ciudad), name="admin_agregar_ciudad"),
    # D&D Management - Geocercas
    #path('geotest', login_required(views.admin_dd_cerca_delictiva), name="admin_dd_cerca_delictiva"),
    path('ajax/get/notificaciones', login_required(views.ajax_get_notificaciones), name = "get_ajax_get_notificaciones"),
    path('d&d-management/dashboard', login_required(views.dashboard_dd), name="dashboard_dd"),
    path('ajax/get/lista_movimientos', login_required(views.ajax_lista_movimientos), name = "get_ajax_lista_movimientos"),
    path('ajax/get/ef_movimientos', login_required(views.ajax_en_tiempo_movimientos), name = "get_en_tiempo_movimientos"),
    path('ajax/get/lista_valorcarga', login_required(views.ajax_lista_valorcarga), name = "get_ajax_lista_valorcarga"),
    path('ajax/get/activos_movimientos', login_required(views.ajax_charts_activos_movimientos), name = "get_ajax_charts_activos_movimientos"),
    path('ajax/get/valor_movimientos', login_required(views.ajax_charts_valor_movimientos), name = "get_ajax_charts_valor_movimientos"),
    path('ajax/get/lista_gpsdevices', login_required(views.ajax_lista_gpsdevices), name = "get_ajax_lista_gpsdevices"), 
    path('ajax/get/fuera_ruta', login_required(views.ajax_fuera_ruta), name = "get_ajax_fuera_ruta"), 
    path('ajax/get/dentro_ruta', login_required(views.ajax_dentro_ruta), name = "get_ajax_dentro_ruta"), 
    path('ajax/get/mov_info_esn', login_required(views.ajax_mov_info_esn), name = "ajax_mov_info_esn"), 
    path('ajax/get/heatmap_movs_activos', login_required(views.ajax_heatmap_movs_activos), name = "ajax_heatmap_movs_activos"), 
    path('ajax/get/heatmap_movs_finalizados', login_required(views.ajax_heatmap_movs_finalizados), name = "ajax_heatmap_movs_finalizados"), 
    path('ajax/get/heatmap_inc_viales', login_required(views.ajax_heatmap_inc_viales), name = "ajax_heatmap_inc_viales"), 
    # E/S Trailers
    path('es-trailers/historial', login_required(views.admin_es_trailers_historial), name="admin_es_trailers_historial"),
    path('es-trailers/ver/<int:estra_id>', login_required(views.admin_es_trailers_ver), name="admin_es_trailers_ver"),     
    


    path('empleados-sin-gafete/lista', login_required(views.admin_empleados_sin_gafete), name="admin_empleados_sin_gafete_lista"),
    path('empleados-sin-gafete/registrar', login_required(views.admin_empleados_sin_gafete_registrar), name="admin_empleados_sin_gafete_registrar"),
       
    path('entradaequipo/lista', login_required(views.admin_entrada_equipo), name="admin_entradaequipo_lista"),
    path('incidentesservicio/lista', login_required(views.admin_incidentes_servicio), name = "admin_incidentes_servicio_lista"),
    path('incidentesservicio/<int:id>', login_required(views.admin_incidentes_servicio_detalle), name="admin_incidentes_servicio_detalle"),
    path('papeletas/', login_required(views.admin_papeletas), name="admin_papeletas"),
    path('papeletas/<int:id>', login_required(views.admin_papeleta_detalle), name="admin_papeleta_detalle"),
    path('papeletas/<int:id>/<int:id_pregunta>', login_required(views.admin_papeleta_nueva_evidencia), name="admin_papeleta_subir_evidencia"),
    path('papeletas/<int:id>/<int:respuesta_id>/recomendacion', login_required(views.admin_papeleta_recomendacion_crear), name="admin_papeleta_recomendacion_crear"),
    path('papeletas/recomendacion/<int:id>', login_required(views.admin_papeleta_recomendacion_edit), name="admin_papeleta_recomendacion_edit"),
    
    #Seccion de Traslados / Movimientos
    
    path('movimientos/crear', login_required(views.MovimientoCreate.as_view()), name="admin_movimientos_crear"),
    path('movimientos/lista', login_required(views.admin_movimientos), name="admin_movimientos_lista"),
    path('movimientos/<int:pk>', login_required(views.MovimientoDetail.as_view()), name="admin_movimientos_detalle"),
    path('movimientos/editar/<int:pk>', login_required(views.MovimientoUpdate.as_view()), name="admin_movimientos_update"),
    path('movimientos/remover/<int:pk>', login_required(views.MovimientoDelete.as_view()), name="admin_movimientos_delete"),
    
    #Tipo De Vehiculo
    path('tipo-de-vehiculo/crear', login_required(views.TipoVehiculoCreateView.as_view()), name="tipo_de_vehiculo_create"),
    path('tipo-de-vehiculo/historial', login_required(views.TipoVehiculoListView.as_view()), name="tipo_de_vehiculo_list"),
    path('tipo-de-vehiculo/<int:pk>', login_required(views.TipoVehiculoDetailView.as_view()), name='tipo_de_vehiculo_detailview'),
    path('tipo-de-vehiculo/editar/<int:pk>/', login_required(views.TipoVehiculoUpdateView.as_view()), name="tipo_de_vehiculo_update"),
    path('tipo-de-vehiculo/borrar/<int:pk>/', login_required(views.TipoVehiculoDelete.as_view()), name="tipo_de_vehiculo_delete"),       

    #Caja
    path('caja/crear', login_required(views.CajaCreateView.as_view()), name="caja_create"),
    path('caja/historial', login_required(views.CajaListView.as_view()), name="caja_list"),
    path('caja/<int:pk>', login_required(views.CajaDetailView.as_view()), name='caja_detailview'),
    path('caja/editar/<int:pk>/', login_required(views.CajaUpdateView.as_view()), name="caja_update"),
    path('caja/borrar/<int:pk>/', login_required(views.CajaDelete.as_view()), name="caja_delete"),

    #Cargas
    path('cargas/crear', login_required(views.CargasCreateView.as_view()), name="cargas_create"),
    path('cargas/historial', login_required(views.CargasListView.as_view()), name="cargas_list"),
    path('cargas/<int:pk>', login_required(views.CargasDetailView.as_view()), name='cargas_detailview'),
    path('cargas/editar/<int:pk>/', login_required(views.CargasUpdateView.as_view()), name="cargas_update"),
    path('cargas/borrar/<int:pk>/', login_required(views.CargasDelete.as_view()), name="cargas_delete"),    
        
    #Choferes    
    path('chofer/crear', login_required(ChoferCreateView.as_view()), name="chofer_create"),
    path('chofer/listado', login_required(ChoferListView.as_view()), name="chofer_list"),
    path('chofer/<int:pk>', login_required(ChoferDetailView.as_view()), name='chofer_detailview'),
    path('chofer/editar/<int:pk>/', login_required(ChoferUpdateView.as_view()), name="chofer_update"),
    path('chofer/borrar/<int:pk>/', login_required(ChoferDelete.as_view()), name="chofer_delete"),
    
    #Vehiculos    
    path('vehiculo/crear', login_required(VehiculoCreateView.as_view()), name="vehiculo_create"),
    path('vehiculo/listado', login_required(VehiculoListView.as_view()), name="vehiculo_list"),
    path('vehiculo/<int:pk>', login_required(VehiculoDetailView.as_view()), name='vehiculo_detailview'),
    path('vehiculo/editar/<int:pk>/', login_required(VehiculoUpdateView.as_view()), name="vehiculo_update"),
    path('vehiculo/borrar/<int:pk>/', login_required(VehiculoDeleteView.as_view()), name="vehiculo_delete"),   

    #GPS Devices    
    path('dispositivos-gps/crear', login_required(GpsDevicesCreateView.as_view()), name="gpsdevices_create"),
    path('dispositivos-gps/listado', login_required(GpsDevicesListView.as_view()), name="gpsdevices_list"),
    path('dispositivos-gps/<int:pk>', login_required(GpsDevicesDetailView.as_view()), name='gpsdevices_detailview'),
    path('dispositivos-gps/editar/<int:pk>/', login_required(GpsDevicesUpdateView.as_view()), name="gpsdevices_update"),
    path('dispositivos-gps/borrar/<int:pk>/', login_required(GpsDevicesDelete.as_view()), name="gpsdevices_delete"),     
    
    # Zona 0
    path('incidentes/dashboard-incidentes', login_required(views.admin_incidentes_dash), name="admin_incidentes_dash"), 
    path('incidentes/incidentes-ajax', login_required(views.admin_incidentes_ajax), name="admin_incidentes_ajax"), 
    path('incidentes/listado-de-incidentes', login_required(views.admin_incidentes_index), name="admin_incidentes_index"), 
    path('incidentes/por-incidente', login_required(views.admin_incidentes_agrupado), name="admin_incidentes_agrupado"), 
    path('incidentes/por-ciudad', login_required(views.admin_incidentes_agrupado_ciudad), name="admin_incidentes_agrupado_ciudad"), 
    path('incidentes/crear', login_required(views.admin_incidentes_create), name = "admin_incidentes_create"),
    path('incidentes/editar/<int:inc_id>', login_required(views.admin_incidentes_edit), name = "admin_incidentes_edit"),
    path('incidentes/remover/<int:inc_id>', login_required(views.admin_incidentes_delete), name = "admin_incidentes_delete"),
    path('incidentes/tipos-de-incidentes', login_required(views.admin_incidentes_tipos), name="admin_incidentes_tipos"), 
    path('incidentes/tipos-de-incidentes/crear', login_required(views.admin_incidentes_tipos_create), name = "admin_incidentes_tipos_create"),
    path('incidentes/tipos-de-incidentes/editar/<int:tipo_id>', login_required(views.admin_incidentes_tipos_edit), name = "admin_incidentes_tipos_edit"),
    path('incidentes/tipos-de-incidentes/remover/<int:tipo_id>', login_required(views.admin_incidentes_tipos_delete), name = "admin_incidentes_tipos_delete"),    
    #AJAX de Zona 0
    path('ajax/get/per_cobertura', login_required(views.ajax_get_per_cobertura), name = "ajax_get_per_cobertura"), 
    #Sección de Análisis de Riesgo
    path('resultados-de-analisis-de-riesgo', login_required(views.admin_resultados_analisis_riesgo), name = "admin_resultados_analisis_riesgo"),
    #Road Map
    path('analisis-de-riego/road-map', login_required(views.admin_analisis_de_riesgo_road_map), name="admin_analisis_de_riesgo_road_map"),
    path('analisis-de-riego/ajax_roadmap_papeletas', login_required(views.ajax_roadmap_tabla), name="ajax_roadmap_papeletas"),
    #Forma de Auditor para Recomendaciones    
    path('analisis-de-riego/revision', login_required(views.admin_analisis_de_riesgo_revision), name="admin_analisis_de_riesgo_revision"),
    path('ajax/analisis-de-riego/vulnerabilidadgral', login_required(views.ajax_vulnerabilidad_general), name="ajax_analisis_de_riesgo_vulnerabilidadgral"),
    path('encuestas/', views.encuestas.as_view(), name="admin_list_encuestas"),
    path('encuestas/crear', views.EncuestaCreate.as_view(), name="admin_create_encuesta"),
    path('encuestas/detalles/<int:pk>', views.EncuestaDetail.as_view(), name="admin_detail_encuesta"),
    path('encuestas/detalles/<int:pk>/pregunta/crear', views.PreguntaCretae.as_view(), name="admin_create_pregunta"),
    path('encuestas/detalles/<int:pk>/pregunta/<int:id>/editar', login_required(views.admin_edit_papeleta), name="admin_edit_pregunta"),
    path('encuestas/detalles/<int:id_encuesta>/pregunta/<int:pk>/eliminar', login_required(views.PreguntaDelete.as_view()), name="admin_delete_pregunta"),
    path('encuestas/editar/<int:pk>', views.EncuestaUpdate.as_view(), name="admin_update_encuesta"),
    path('encuestas/eliminar/<int:pk>', views.EncuestaDelete.as_view(), name="admin_delete_encuesta"),
    path('encuestas/categorias/crear', views.CategoriaEncuestaCreate.as_view(), name="admin_create_categoria"),
    path('encuestas/categorias', views.CategoriasEncuesta.as_view(), name="admin_list_categorias"),
    path('encuestas/categorias/editar/<int:pk>', views.CategoriaUpdate.as_view(), name="admin_update_categoria"),    
    #path('encuestas/analisis', views.AnalisisEncuesta.as_view(), name="admin_list_analisis"),
    #path('encuestas/analisis/crear', views.AnalisisEncuestaCreate.as_view(), name="admin_create_analisis"),
    #path('encuestas/analisis/editar/<int:pk>', views.AnalisisUpdate.as_view(), name="admin_update_analisis"),

    path('geocerca-planta/<int:pk>', login_required(views.mapa_geocercas), name="admin_geocerca" ), 
    path('ajax-lastracking', login_required(views.ajax_last_tracking), name="admin_ajax_last_tracking"), 

    # Formato Registro de Visitantes
    path('visitantes/historial', login_required(views.admin_visitantes_index), name="admin_visitantes_index"),
    path('visitantes/crear', login_required(views.admin_visitantes_create), name="admin_visitantes_create"),
    path('visitantes/editar/<int:pk>', login_required(views.admin_visitantes_show), name="admin_visitantes_show"),   

    # Formato Registro de Visitantes
    path('recibo-almacen/historial', login_required(views.admin_recibo_almacen_index), name="admin_recibo_almacen_index"),
    path('recibo-almacen/crear', login_required(views.admin_recibo_almacen_create), name="admin_recibo_almacen_create"),
    path('recibo-almacen/ver/<int:pk>', login_required(views.admin_recibo_almacen_show), name="admin_recibo_almacen_show"),   
    path('recibo-almacen/editar/<int:pk>', login_required(views.admin_recibo_almacen_edit), name="admin_recibo_almacen_edit"),
    path('recibo-almacen/borrar/<int:pk>', login_required(views.admin_recibo_almacen_delete), name="admin_recibo_almacen_delete"),   
    path('ajax/get/recibo_items', login_required(views.admin_recibo_almacen_ajax_search), name = "admin_recibo_almacen_ajax_search"),
    
    #Visitantes
    #path('visitantes/crear', login_required(views.VisitantesCreateView.as_view()), name="visitantes_create"),
    #path('visitantes/historial', login_required(views.VisitantesListView.as_view()), name="visitantes_list"),
    #path('visitantes/<int:pk>', login_required(views.VisitantesDetailView.as_view()), name='visitantes_detailview'),
    #path('visitantes/editar/<int:pk>/', login_required(views.VisitantesUpdateView.as_view()), name="visitantes_update"),
    #path('visitantes/borrar/<int:pk>/', login_required(views.VisitantesDelete.as_view()), name="visitantes_delete"),    

    #Proveedores
    #path('proveedores/listado', login_required(views.admin_proveedores_index), name="admin_proveedores_index"), 
    #path('proveedores/crear', login_required(views.admin_proveedores_create), name="admin_proveedores_create"), 
    #path('proveedores/editar/<int:prov_id>', login_required(views.admin_proveedores_edit), name = "admin_proveedores_edit"),
    #path('proveedores/remover/<int:prov_id>', login_required(views.admin_proveedores_delete), name = "admin_proveedores_delete"),    
    
    #Proveedores
    path('proveedores/crear', login_required(views.ProveedorCreateView.as_view()), name="proveedores_create"),
    path('proveedores/historial', login_required(views.ProveedorListView.as_view()), name="proveedores_list"),
    path('proveedores/<int:pk>', login_required(views.ProveedorDetailView.as_view()), name='proveedores_detailview'),
    path('proveedores/editar/<int:pk>/', login_required(views.ProveedorUpdateView.as_view()), name="proveedores_update"),
    path('proveedores/borrar/<int:pk>/', login_required(views.ProveedorDelete.as_view()), name="proveedores_delete"),

    #Logros
    path('logros/crear', login_required(views.LogroCreateView.as_view()), name="logros_create"),
    path('logros/historial', login_required(views.LogroListView.as_view()), name="logros_list"),
    path('logros/<int:pk>', login_required(views.LogroDetailView.as_view()), name='logros_detailview'),
    path('logros/editar/<int:pk>/', login_required(views.LogroUpdateView.as_view()), name="logros_update"),
    path('logros/borrar/<int:pk>/', login_required(views.LogroDelete.as_view()), name="logros_delete"),  

    #Unidad de Negocio
    path('unidad-de-negocio/crear', login_required(views.PlantaCreateView.as_view()), name="unidad_de_negocio_create"),
    #path('unidad-de-negocio/historial', login_required(views.PlantaListView.as_view()), name="unidad_de_negocio_list"),
    path('unidad-de-negocio/<int:pk>', login_required(views.PlantaDetailView.as_view()), name='unidad_de_negocio_detailview'),
    #path('unidad-de-negocio/editar/<int:pk>/', login_required(views.PlantaUpdateView.as_view()), name="unidad_de_negocio_update"),
    path('unidad-de-negocio/borrar/<int:pk>/', login_required(views.PlantaDelete.as_view()), name="unidad_de_negocio_delete"),
    
    #GPS
    #path('gpstracking/crear', login_required(views.GPSTrackingCreateView.as_view()), name="gpstracking_create"),
    #path('gpstracking/historial', login_required(views.GPSTrackingListView.as_view()), name="gpstracking_list"),
    #path('gpstracking/<int:pk>', login_required(views.GPSTrackingDetailView.as_view()), name='gpstracking_detailview'),
    #path('gpstracking/editar/<int:pk>/', login_required(views.GPSTrackingUpdateView.as_view()), name="gpstracking_update"),
    #path('gpstracking/borrar/<int:pk>/', login_required(views.GPSTrackingDelete.as_view()), name="gpstracking_delete"),      
   
    #ceo_master_modulo_general
    path('ajax/get/ceo_numero_rondines', login_required(views.ajax_ceo_numero_rondines), name="get_ajax_ceo_numero_rondines"),
    path('ajax/get/ceo_numero_incidentes_rondines', login_required(views.ajax_ceo_numero_incidentes_rondines), name="get_ajax_ceo_numero_incidentes_rondines"),
    path('ajax/get/ceo_recomendaciones', login_required(views.ajax_ceo_recomendaciones), name="get_ajax_ceo_recomendaciones"),
    path('ajax/get/ceo_18_puntos', login_required(views.ajax_ceo_18_puntos), name="get_ajax_ceo_18_puntos"),
    path('ajax/get/ceo_personal_sin_gafete', login_required(views.ajax_ceo_personal_sin_gafete), name="get_ajax_ceo_personal_sin_gafete"),
    path('ajax/get/num_visitantes', login_required(views.ajax_num_visitantes), name="get_ajax_num_visitantes"),
    path('ajax/get/ponderacion', login_required(views.ajax_ponderacion), name="get_ajax_ponderacion"),
    path('ajax/get/capacitacion', login_required(views.ajax_capacitacion), name="get_ajax_capacitacion"),
    path('ajax/get/cobertura_planta', login_required(views.ajax_cobertura_planta), name="get_ajax_cobertura_planta"),
    path('ajax/get/ceo_capacitacion', login_required(views.ajax_ceo_capacitacion), name="get_ajax_ceo_capacitacion"),
    
    path('news_rss', login_required(views.news_rss), name="news_rss"), 

    path('reporte-analisis-riesgo', generate_pdf_analisis_riesgo.as_view(), name="generate_pdf_analisis_riesgo"),   
    path('reporte-predictive', generate_pdf_predictive.as_view(), name="generate_pdf_predictive"),  

], 'administrador')   
