from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from entorno.models import Incidente
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from core import user_validation
from django.http import HttpResponseRedirect
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from core.forms import PlantaForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

class PlantaListView(ListView):
    model = Planta    
    template_name = 'administrador/unidad_de_negocio/unidad_de_negocio_list.html'   
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        return context 
    
class PlantaDetailView(DetailView):
    model = Planta    
    template_name = 'administrador/unidad_de_negocio/unidad_de_negocio_detail.html' 
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        return context
    
class PlantaUpdateView(UpdateView):
    model = Planta    
    form_class = PlantaForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/unidad_de_negocio/unidad_de_negocio_update_form.html'    
    
    def get_success_url(self):
        return reverse_lazy('administrador:unidad_de_negocio_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        return context
    
class PlantaCreateView(CreateView):
    model = Planta        
    form_class = PlantaForm 
    template_name = 'administrador/unidad_de_negocio/unidad_de_negocio_form.html'        
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:admin_un_index')

    def form_valid(self, form, **kwargs):        
        form = form.save(commit=False)
        if form.alias == None:            
            form.alias = slugify(form.alias)             
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):        
        js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar',  'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_unidad_negocio_crear' ] 
        context = super().get_context_data(**kwargs)
        context['css_list'] = css_list
        context['js_list'] = js_list                
        return context
        
    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        self.object = None
        form = form_class(request=request)
        return self.render_to_response(self.get_context_data(form=form))

class PlantaDelete(DeleteView):
    model = Planta        
    template_name = 'administrador/unidad_de_negocio/unidad_de_negocio_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:admin_un_index')  
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        return context