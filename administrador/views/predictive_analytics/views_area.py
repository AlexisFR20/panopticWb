from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from analytics.forms import  AreaRestringidaForm
from analytics.models import Area_Restringida
from django.urls import reverse, reverse_lazy

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_datetimepicker']

#Vistas de Registro de Paquetería
class AreaListView(ListView):
    model = Area_Restringida    
    template_name = 'administrador/predictive/area_list.html'   
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class AreaDetailView(DetailView):
    model = Area_Restringida    
    template_name = 'administrador/predictive/area_detail.html' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class AreaUpdateView(UpdateView):
    model = Area_Restringida    
    form_class = AreaRestringidaForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/predictive/area_update_form.html'    
    
    def get_success_url(self):
        return reverse_lazy('administrador:area_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class AreaCreateView(CreateView):
    model = Area_Restringida        
    form_class = AreaRestringidaForm 
    template_name = 'administrador/predictive/area_form.html'    
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:area_list')   
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class AreaDelete(DeleteView):
    model = Area_Restringida        
    template_name = 'administrador/predictive/area_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:area_list')  
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context