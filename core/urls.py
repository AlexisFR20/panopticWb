from django.conf.urls import handler404, handler500
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.conf import settings
# importamos las vistas creadas en CORE
from administrador import urls
from . import views
from .views import GeneratePDF3
from core.utils import *

css_list = ['basic', 'slick', 'custom']
js_list = ['js_basic', 'js_slick']

urlpatterns = [
    # Frontend Routes
    #path('', views.login, name="login"),
    #path('', views.CustomLoginView.as_view(extra_context = { 'css_list': css_list, 'js_list': js_list }), name="login"),
    #path('accounts/login/', auth_views.LoginView.as_view(extra_context = { 'css_list': css_list, 'js_list': js_list }), name="outlogin"),
    #path('accounts/login/', views.LoginCustom.as_view(extra_context = { 'css_list': css_list, 'js_list': js_list }), name="login"),
    #path('', login_required(views.home), name="inicio"),  
    path('',  login_required(views.ceo_global), name="inicio"),  
    path('accounts/', include('django.contrib.auth.urls')),        
    path('logout', auth_views.LogoutView.as_view(extra_context = { 'css_list': css_list, 'js_list': js_list }), name="logout"),
    path('inicio', login_required(views.home), name="inicio"),  
    path('layout', login_required(views.layout), name="layout"), 
    #Informe total
    path('informe_total', login_required(views.informe_total), name="informe_total"),
    #Vistas DEMO Prediictive
    path('ceo/dashboard', views.ceo_dashboard, name="ceo_dashboard"),   
    #Vistas DEMO Prediictive
    path('ceo/dashboard', views.ceo_dashboard, name="ceo_dashboard"),   
    path('ceo', views.ceo, name="ceo"),  
    path('ceo_global', login_required(views.ceo_global), name="ceo_global"),  
    path('ceo_pais', login_required(views.ceo_pais), name="ceo_pais"),  
    path('ceo_master', login_required(views.ceo_master), name="ceo_master"),  
    path('ceo_master/modulo_general', login_required(views.ceo_master_modulo_general), name="ceo_master_modulo_general"),  
    path('ceo_master/yazaki_benito_juarez', login_required(views.ceo_master_yz_benito_juarez), name="ceo_master_yz_benito_juarez"),  
    path('ceo_detalle', login_required(views.ceo_detalle), name="ceo_detalle"),  
    path('vice_global', login_required(views.vice_global), name="vice_global"),  
    path('vice_pais', login_required(views.vice_pais), name="vice_pais"),  
    path('vice_master', login_required(views.vice_master), name="vice_master"),  
    path('vice_master/modulo_general', login_required(views.vice_master_modulo_general), name="vice_master_modulo_general"),  
    path('ceo_master/progreso_incidentes', login_required(views.progreso_incidentes), name="progreso_incidentes"),
    path('vice_master/yazaki_benito_juarez', login_required(views.vice_master_yz_benito_juarez), name="vice_master_yz_benito_juarez"),  
    path('vice_detalle', login_required(views.vice_detalle), name="vice_detalle"),  
    path('vicela_global', login_required(views.vicela_global), name="vicela_global"),  
    path('vicela_pais', login_required(views.vicela_pais), name="vicela_pais"),  
    path('vicela_master', login_required(views.vicela_master), name="vicela_master"),  
    path('vicela_detalle', login_required(views.vicela_detalle), name="vicela_detalle"),  
    path('gtereg_global', login_required(views.gtereg_global), name="gtereg_global"),  
    path('gtereg_pais', login_required(views.gtereg_pais), name="gtereg_pais"),  
    path('gtereg_master', login_required(views.gtereg_master), name="gtereg_master"),  
    path('gtereg_detalle', login_required(views.gtereg_detalle), name="gtereg_detalle"), 
    path('gteplanta_global', login_required(views.gteplanta_global), name="gteplanta_global"),  
    path('gteplanta_pais', login_required(views.gteplanta_pais), name="gteplanta_pais"),  
    path('gteplanta_master', login_required(views.gteplanta_master), name="gteplanta_master"),  
    path('gteplanta_detalle', login_required(views.gteplanta_detalle), name="gteplanta_detalle"), 
    path('gteplus_global', login_required(views.gteplus_global), name="gteplus_global"),  
    path('gteplus_pais', login_required(views.gteplus_pais), name="gteplus_pais"),  
    path('gteplus_master', login_required(views.gteplus_master), name="gteplus_master"),  
    path('gteplus_detalle', login_required(views.gteplus_detalle), name="gteplus_detalle"),  
    #path('ceo_global', views.ceo_global, name="ceo_global"),  
    path('dash_plantas', views.home_plantas, name="dash_plantas"),  
    # path ('ruta-de-navegador', views.funcion_def_en_views, name="")    
    path('widgets/graficas/plotly/histograma', views.swidgets_plotly_histograma, name="plotly_histograma"),
    path('widgets/graficas/plotly/barchart_simple_vertical', views.swidgets_plotly_barchart_simple_vertical, name="plotly_barchart_simple_vertical"),
    path('widgets/graficas/plotly/barchart_simple_vertical_etiquetas_fijas', views.swidgets_plotly_barchart_simple_vertical_etiquetas_fijas, name="plotly_barchart_simple_vertical_etiquetas_fijas"),
    path('widgets/graficas/plotly/barchart_grupo_vertical', views.swidgets_plotly_barchart_grupo_vertical, name="plotly_barchart_grupo_vertical"),
    path('widgets/graficas/plotly/barchart_grupo_horizontal', views.swidgets_plotly_barchart_grupo_horizontal, name="plotly_barchart_grupo_horizontal"),
    path('widgets/graficas/plotly/barchart_grupo_horizontal_lbls_inclinadas', views.swidgets_plotly_barchart_grupo_horizontal_lbls_inclinadas, name="plotly_barchart_grupo_horizontal_lbls_inclinadas"),
    path('widgets/graficas/plotly/barchart_ancho_individual', views.swidgets_plotly_barchart_ancho_individual, name="plotly_barchart_grupo_horizontal_ancho_individual"),
    path('widgets/graficas/plotly/barchart_color_individual', views.swidgets_plotly_barchart_color_individual, name="plotly_barchart_color_individual"),
    path('widgets/graficas/plotly/barchart_estilizada', views.swidgets_plotly_barchart_estilizada, name="plotly_barchart_estilizada"),
    path('dashdemo', views.dashdemo22, name="plotly_dashdemo"),
    path('testpdf', GeneratePDF3.as_view(), name="testpdf"),         
    path('pagina-no-encontrada', views.redirect404, name="redirect404template"),

    path('mapa-de-calor', login_required(views.mapa_calor), name="mapa_calor"),  
    path('news_rss', views.news_rss, name="news_rss"),         
]

#handler404 = 'core.views.error_404_view'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
