from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from ddmanagement.models import gpsdevice
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ddmanagement.forms import GpsDevicesForm
from django.urls import reverse, reverse_lazy

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_datetimepicker']

#Vistas de Registro de Paquetería
class GpsDevicesListView(ListView):
    model = gpsdevice
    template_name = 'administrador/ddmanagement/gpsdevices/gpsdevices_list.html'       
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        context['cliente_user'] = self.request.user.cliente
        return context 
    
class GpsDevicesDetailView(DetailView):
    model = gpsdevice    
    template_name = 'administrador/ddmanagement/gpsdevices/gpsdevices_detail.html' 
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class GpsDevicesUpdateView(UpdateView):
    model = gpsdevice    
    form_class = GpsDevicesForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/ddmanagement/gpsdevices/gpsdevices_update_form.html'        
    
    def get_success_url(self):        
        return reverse_lazy('administrador:gpsdevices_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)                
        context['css_list'] = css_list
        context['js_list'] = js_list       
        context['cliente_user'] = self.request.user.cliente
        return context 
    
class GpsDevicesCreateView(CreateView):
    model = gpsdevice        
    form_class = GpsDevicesForm 
    template_name = 'administrador/ddmanagement/gpsdevices/gpsdevices_form.html'          
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:gpsdevices_list')
    
    def get_context_data(self, **kwargs):
        #print(self.)
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        
        context['cliente_user'] = self.request.user.cliente
        return context

class GpsDevicesDelete(DeleteView):
    model = gpsdevice        
    template_name = 'administrador/ddmanagement/gpsdevices/gpsdevices_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:gpsdevices_list')  
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context