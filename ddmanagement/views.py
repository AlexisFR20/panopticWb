from django.shortcuts import render, HttpResponse
from core import user_validation
from django.views.generic import  DetailView
from ddmanagement.models import *
from core.models import Notificacion
from entorno.models import Incidente, TipoIncidente
import datetime as dt

n = Notificacion.objects.filter(visto = False)

css_list =  ['basic', 'slick', 'metismenu', 'mapbox', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_gps_all' ]

# Create your views here.
def home(request):    
    
    movs = Movimiento.objects.all()    
    qmovs = Movimiento.objects.all().count()
    
    #Verifica que esté definido vcliene 
    if 'vcliente' in request.session:
        vcliente = request.session['vcliente']             
        vplantas = Planta.objects.filter(cliente=vcliente['id'])
        vmovimientos = Movimiento.objects.filter()
    else:
        vcliente = None
        vplantas = None
    
    return render(request, 'ddmanagement/newhome.html', {"css_list": css_list, "js_list": js_list, 'movs': movs, 'qmovs': qmovs,  'vcliente': vcliente, 'vplantas': vplantas })

def home_planta(request, id):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = id
    #print("from view: "+str(userdict))
    request.session['django_plotly_dash'] = dash_context    
    return render(request, 'ddmanagement/home.html', {"css_list": css_list, "js_list": js_list, 'userdict': userdict})

class MovimientoDetail(DetailView):
    model = Movimiento
    template_name = 'ddmanagement/movimiento_detail.html'
    
    def get(self, *args, **kwargs):
        self.object = self.get_object()
        movimiento = Movimiento.objects.get(pk=self.object.id)       
                
        return super(MovimientoDetail, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox', 'js_gps_new']
        context['css_list'] = css_list
        context['js_list'] = js_list
        context['notificaciones'] = n 
        tickets = self.object.movimiento_tickets.all()
        context['tickets'] = tickets
        context['notificaciones'] = n
        incidentes = self.object.incidentevial_set.all()
        context['incidentes'] = incidentes
        
        #RANGO DE FECHA
        till = dt.date.today()
        if till.month == 1:
            fr = till.replace(month = 12, year = till.year - 1)
        else:
            fr = till.replace(month = till.month - 1)

        incidentesMapa = Incidente.objects.filter(fecha__range=[fr,till])
        context['incidentesMapa'] = incidentesMapa
        tipo_incidente = TipoIncidente.objects.all()
        context['tipoincidentes'] = tipo_incidente
        
        return context
    
