from django.shortcuts import render, HttpResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableView, RequestConfig, tables
from django.urls import reverse, reverse_lazy
from .tables import EncuestaTable, PreguntaTable, PapeletaTable, RespuestaTable
from .models import Encuesta, Categoria_Encuesta, Pregunta, Papeleta, Respuesta, Recomendacion
from core.models import Cliente, Planta
from .forms import EncuestaForm, PreguntaForm, PapeletaForm, RecomendacionForm
from . import charts
from core import user_validation


css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']


# Create your views here.
def home(request):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = None
    #print("from view: "+str(userdict))
    request.session['django_plotly_dash'] = dash_context

    return render(request, "arnes/home.html", { 'css_list': css_list, 'js_list': js_list, "userdict": userdict,
    })

def home_planta(request, id):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']

    userdict = user_validation.validate(request)
    dash_context = request.session.get("django_plotly_dash", dict())
    dash_context['userdict'] = userdict
    dash_context['planta_id'] = id
    request.session['django_plotly_dash'] = dash_context

    return render(request, "arnes/home.html", { 'css_list': css_list, 'js_list': js_list, "userdict": userdict,
    })

class CategoriaEncuestaCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Categoria_Encuesta
    fields = ["nombre"]
    
    def get_success_url(self):
        return reverse('arnes:list_encuestas')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class EncuestaCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Encuesta
    form_class = EncuestaForm
    
    def get_success_url(self):
        return reverse('arnes:detail_encuesta', args=[self.object.id])
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class EncuestaDetail(DetailView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Encuesta

    def get_context_data(self, **kwargs):
        preguntas = Pregunta.objects.filter(encuesta_id=self.object.id)
        papeletas = Papeleta.objects.filter(encuesta_id=self.object.id)
        table = PreguntaTable(preguntas)
        tpapeletas = PapeletaTable(papeletas)
        RequestConfig(self.request, paginate=False).configure(table)
        RequestConfig(self.request, paginate=False).configure(tpapeletas)
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['table'] = table
        context['tpapeletas'] = tpapeletas
        return context

class EncuestaUpdate(UpdateView):
    model = Encuesta
    form_class = EncuestaForm
    template_name = 'arnes/encuesta_update_form.html'

    def get_success_url(self):
        return reverse_lazy('arnes:update_encuesta', args=[self.object.id]) + '?ok'

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class EncuestaDelete(DeleteView):
    model = Encuesta
    success_url = reverse_lazy('arnes:list_encuestas')

    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class encuestas(SingleTableView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    
    table_class = EncuestaTable
    template_name = 'arnes/list_encuestas.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        lista = None
        if query != '':
            lista = Encuesta.objects.filter(nombre__contains=query)
        else:
            lista = Encuesta.objects.all()
        return lista

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        return context

class PreguntaCretae(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Pregunta
    form_class = PreguntaForm
    
    def get_success_url(self, **kwargs):
        return reverse('arnes:detail_encuesta', kwargs={'pk': self.kwargs.get("pk")} )

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))

        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['pk'] = self.kwargs.get("pk")

        return context

class PapeletaCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model = Papeleta
    form_class = PapeletaForm

    def get_success_url(self, **kwargs):
        return reverse('arnes:detail_encuesta', kwargs={'pk': self.kwargs.get("pk")} )

    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)
        form.encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))
        form.user_aguilas = self.request.user
        
        preg=self.request.POST.getlist("preguntaid[]")
        pregtext=self.request.POST.getlist("preguntatext[]")
        resp=self.request.POST.getlist("respuesta[]")
        cump=self.request.POST.getlist("cumple[]")
        ocu=self.request.POST.getlist("ocurrencia[]")
        imp=self.request.POST.getlist("impacto[]")
        result=self.request.POST.getlist("resultado[]")
        obs=self.request.POST.getlist("observaciones[]")
        print("POST: " + str(self.request.POST))
        form.save()
        print("papeleta " + str(form))

        for i in range(0,len(resp)):
            respuesta = Respuesta()
            respuesta.pregunta_id = preg[i]
            pregunta = Pregunta.objects.get(id=preg[i])
            respuesta.pregunta_text = pregunta.pregunta
            respuesta.repuesta = resp[i]
            respuesta.cumple = cump[i]
            respuesta.ocurrencia = ocu[i]
            respuesta.impacto = ocu[i]
            respuesta.resultado = result[i]
            respuesta.observacion = obs[i]
            print("res: "+str(resp[i])+", ocu: "+str(ocu[i]))
            respuesta.papeleta = form
            respuesta.save()


        #form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books      
        encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))  
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['encuesta'] = encuesta
        context['pk'] = self.kwargs.get("pk")

        return context

class RecomendacionCreate(CreateView):
    css_list = ['basic', 'metismenu', 'perfectscrollbar', 'custom']
    js_list = ['js_basic', 'js_metismenu', 'js_perfectscrollbar']
    model=Recomendacion
    form_class = RecomendacionForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books      
        encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))  
        context['css_list'] = self.css_list
        context['js_list'] = self.js_list
        context['pk'] = self.kwargs.get("pk")

        return context

class PapeletaDetail(DetailView):
    
    model = Papeleta

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def papeletas(request):    
    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        papeletas = Papeleta.objects.all().order_by('fecha').reverse()
    elif(request.user.getRolU() == "auditor"):
        papeletas = Papeleta.objects.filter(user_aguilas=request.user).all()
        plantas_ids = []
        clientes_ids = []
        for p in papeletas:
            if p.planta_id not in plantas_ids:
                plantas_ids.append(p.planta_id)
                print("agregada Planta "+str(p.planta_id))

            if p.planta.cliente_id not in clientes_ids:
                clientes_ids.append(p.planta.cliente_id)
                print("Agregado Cliente "+str(p.planta.cliente_id))

        plantas = Planta.objects.filter(id__in=plantas_ids).all()
        clientes = Cliente.objects.filter(id__in=clientes_ids)
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
        

    if not (request.GET.get("todas")):
        papeletas = filterEncuestas(papeletas)

    return render(request, 'arnes/papeleta_lista.html', { 'css_list': css_list, 'js_list': js_list, 'papeletas': papeletas })

def roadmap(request): 
    #analisis = Analisis.objects.all()
    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        #papeletas = Papeleta.objects.all().order_by('fecha').reverse()
        #papeletas = filterEncuestas(papeletas)
    elif(request.user.getRolU() == "auditor"):
        #papeletas = Papeleta.objects.filter(user_aguilas=request.user).all()
        #papeletas = filterEncuestas(papeletas)
        #plantas_ids = []
        #clientes_ids = []
        #for p in papeletas:
        #    if p.planta_id not in plantas_ids:
        #        plantas_ids.append(p.planta_id)
        #        print("agregada Planta "+str(p.planta_id))

        #    if p.planta.cliente_id not in clientes_ids:
        #        clientes_ids.append(p.planta.cliente_id)
        #        print("Agregado Cliente "+str(p.planta.cliente_id))

        #plantas = Planta.objects.filter(id__in=plantas_ids).all()
        #clientes = Cliente.objects.filter(id__in=clientes_ids)
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        #papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
        #papeletas = filterEncuestas(papeletas)
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        #papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
        #papeletas = Papeleta.objects.filter(planta_id=request.user.planta_id).all().order_by('-fecha') 
        #papeletas = filterEncuestas(papeletas)

    return render(request, 'arnes/roadmap.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes})


def ajax_roadmap_tabla(request):
    planta = request.GET.get("planta_id")
    cliente = request.GET.get("cliente_id")
    #analisis = request.GET.get("analisis_id")

    if planta != "":
        #papeletas = Papeleta.objects.filter(planta_id=planta).filter(encuesta__categoria__analisis_id = analisis).all().order_by('-fecha')
        papeletas = Papeleta.objects.filter(planta_id=planta).all().order_by("-fecha")
    else:
        papeletas = Papeleta.objects.filter(planta__cliente_id=cliente).all().order_by("-fecha")
        #papeletas = Papeleta.objects.filter(planta__cliente_id=cliente).filter(encuesta__categoria__analisis_id = analisis).all().order_by('-fecha')

    return render(request, 'arnes/ajax_road_map_table_papeletas.html', {'papeletas': papeletas })


def filterEncuestas(papeletas):
    #get distings plantas
    plantas_ids = []
    for p in papeletas:
        if p.planta_id not in plantas_ids:
            plantas_ids.append(p.planta_id)
            #print("agregada Planta "+str(p.planta_id))


    pencuestas = []
    pencuestas_ids = []
    p_ids = []
    #for each planta
    for pid in plantas_ids:
        #print("evaluando Planta "+str(pid))
        pfiltered = papeletas.filter(planta_id=pid)
        #each papelete in planta
        
        pencuestas_ids = []
        #tomar encuesta mas reciente de cada una diferente
        for penc in pfiltered.order_by("encuesta_id", "-fecha"):
            #print("evaluando "+str(penc.encuesta_id))
            if penc.encuesta_id not in pencuestas_ids:
                pencuestas.append(penc)
                #print("papeleta "+str(penc.id))
                p_ids.append(penc.id)
                pencuestas_ids.append(penc.encuesta_id)
                #print("agregada "+str(penc))
            
    #print("pids "+str(p_ids))
    #print("enc_ids "+str(pencuestas_ids))
    #print("papeletas "+str(pencuestas))
    #papeletas filtradas por la mas recientes de cada tipo
    papeletas = papeletas.filter(id__in=p_ids).all()

    return papeletas

def resultados_analisis_riesgo(request):
    if(request.user.getRolU() == "administrador"):
        clientes = Cliente.objects.all()
        plantas = Planta.objects.all()
        #papeletas = Papeleta.objects.all().order_by('fecha').reverse()
        #papeletas = filterEncuestas(papeletas)
    elif(request.user.getRolU() == "auditor"):
        papeletas = Papeleta.objects.filter(user_aguilas=request.user).all()
        papeletas = filterEncuestas(papeletas)
        plantas_ids = []
        clientes_ids = []
        for p in papeletas:
            if p.planta_id not in plantas_ids:
                plantas_ids.append(p.planta_id)
                print("agregada Planta "+str(p.planta_id))

            if p.planta.cliente_id not in clientes_ids:
                clientes_ids.append(p.planta.cliente_id)
                print("Agregado Cliente "+str(p.planta.cliente_id))

        plantas = Planta.objects.filter(id__in=plantas_ids).all()
        clientes = Cliente.objects.filter(id__in=clientes_ids)
    elif(request.user.getRolU() == "ceo"):
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
        
    else:
        clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
        plantas = Planta.objects.filter(id=request.user.planta_id).all()
        

    return render(request, 'arnes/resultados_analisis_riesgo.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes })


