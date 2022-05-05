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
from unicodedata import name
from django.urls import path
from django.contrib.auth.decorators import login_required
# importamos las vistas creadas en CORE
from . import views

cporte_patterns = ([
    # Frontend Routes
    path('clientes/crear', login_required(views.PorteClienteCreateView.as_view()), name="porte_cliente_create"),
    #path('productos/crear', login_required(views.porteProducto), name="porte_producto_create"),
    #path('productos/remover/<str:id>', login_required(views.porteProductoDelete), name="porte_producto_delete"),
    #path('productos/editar/<str:id>', login_required(views.porteProductoUpdate), name="porte_producto_update"),
    #path('productos', login_required(views.porteProductoList), name="porte_producto_list"),
    path('receiver/crear', login_required(views.PorteReceiverCreateView.as_view()), name="porte_receiver_create"),
    path('receiver/remover/<int:id>', login_required(views.porteReceiverDelete), name="porte_receiver_delete"),
    path('receiver/editar/<int:pk>', login_required(views.PorteReceiverUpdate.as_view()), name="porte_receiver_update"),
    path('receiver', login_required(views.porteReceiverList), name="porte_receiver_list"),
    path('facturas/crear',login_required(views.porteFactura), name="porte_factura_create"),
    path('facturas/editar/<int:id>', login_required(views.porteFacturaUpdate), name="porte_factura_update"),
    path('facturas/eliminar/<int:id>', login_required(views.porteFacturaDelete), name="porte_factura_delete"),
    path('facturas',login_required(views.porteFacturaList), name="porte_factura_list"),
    path('codigopostal',login_required(views.getPostalCode),name="get_cp"),
    path('codigounidades', login_required(views.getProductoServicioCode),name="get_unidades"),
    path('claveproducto',login_required(views.getClaveProducto),name="get_clave"),
    path('ubicacion', login_required(views.getUbicacion),name="get_ubicacion"),
    path('figuras',login_required(views.porteFiguraList), name="porte_figura_list"),
    path('figuras/crear',login_required(views.porteFiguraCreate),name="porte_figura_create"),
    path('figuras/get', login_required(views.ajax_get_figura), name="get_figura"),
    path('figuras/editar/<int:id>',login_required(views.updateFigura), name="porte_figura_update"),
    path('cliente/permiso', login_required(views.updatePermiso), name="porte_permiso_update"),
    path('codigoremolques', login_required(views.getTipoRemolques), name="get_tipo_remolques")
], 'cporte')
