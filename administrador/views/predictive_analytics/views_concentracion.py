from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from analytics.forms import ConcentracionForm
from analytics.models import Concentracion 
from django.urls import reverse, reverse_lazy

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker', 'js_datetimepicker' ]

class ConcentracionListView(ListView):
    model = Concentracion    
    template_name = 'administrador/predictive/concentracion_list.html'   
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class ConcentracionDetailView(DetailView):
    model = Concentracion    
    template_name = 'administrador/predictive/concentracion_detail.html' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class ConcentracionUpdateView(UpdateView):
    model = Concentracion    
    form_class = ConcentracionForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/predictive/concentracion_update_form.html'    
    
    def get_success_url(self):
        return reverse_lazy('administrador:concentracion_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class ConcentracionCreateView(CreateView):
    model = Concentracion        
    form_class = ConcentracionForm 
    template_name = 'administrador/predictive/concentracion_form.html'    
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:concentracion_list')

    def form_valid(self, form, **kwargs):
        #plantaID = self.request.user.planta.id        
        form = form.save(commit=False)        
        #form.encuesta = Encuesta.objects.get(pk=self.kwargs.get("pk"))        
        #form.un = self.request.user.planta
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class ConcentracionDelete(DeleteView):
    model = Concentracion        
    template_name = 'administrador/predictive/concentracion_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:concentracion_list')  
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context