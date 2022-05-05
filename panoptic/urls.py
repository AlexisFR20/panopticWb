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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
# importamos las vistas creadas en CORE
from core import views
from entorno.urls import entorno_patterns
from arnes.urls import arnes_patterns
from analytics.urls import analytics_patterns
from ddmanagement.urls import ddmanagement_patterns
from administrador.urls import administrador_patterns
from cporte.urls import cporte_patterns
from API.urls import api_patterns
import django_plotly_dash
from core.dash_apps import simpleexample
from core.dash_apps import histograma_delitos
from core.dash_apps import dash_plantas
from core.dash_apps import dash_zona0
from core.dash_apps import dash_analytics
from core.dash_apps import dash_arnes
from core.dash_apps import dash_ddmanagement

urlpatterns = [
    # Frontend Routes
    path('', include('core.urls')),
    path('entorno/', include(entorno_patterns)),
    path('analytics/', include(analytics_patterns)),
    path('arnes/', include(arnes_patterns)),
    path('ddmanagement/', include(ddmanagement_patterns)),
    path('backstage/', include(administrador_patterns)),
    path('api/', include(api_patterns)),
    path('cporte/', include(cporte_patterns)),
    # Backend Routes
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),    
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    urlpatterns = [path('__debug__/', include(debug_toolbar.urls)),] + urlpatterns

handler404 = 'core.views.error_404_view'
