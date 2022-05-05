from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ddmanagement.forms import VehiculoForm
from ddmanagement.models import Vehiculo, gpsdevice
from ddmanagement.models import TipoVehiculo
from django.urls import reverse, reverse_lazy
#from django.utils.text import slugify

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_datetimepicker']

class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'administrador/ddmanagement/vehiculos/vehiculo_list.html'   
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class VehiculoCreateView(CreateView): 
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'administrador/ddmanagement/vehiculos/vehiculo_form.html'

    def get_success_url(self):
        return reverse_lazy('administrador:vehiculo_list') + '?ok'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

def admin_vehiculos(request):

    vehiculos = Vehiculo.objects.all()

    return render(request, 'administrador/ddmanagement/vehiculos/vehiculos_lista.html', { 'css_list': css_list, 'js_list': js_list, 'vehiculos': vehiculos })

class VehiculoDetailView(DetailView):
    model = Vehiculo
    template_name = 'administrador/ddmanagement/vehiculos/vehiculo_detail.html'

    def get_context_data(self, **kwargs):
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'administrador/ddmanagement/vehiculos/vehiculo_update_form.html'    

    def get_success_url(self, **kwargs):
        return reverse_lazy('administrador:vehiculo_update', args=[self.kwargs.get("pk")]) + '?ok'
    
    def form_valid(self, form, **kwargs):
        form = form.save(commit=False)        
        self.object.id = self.kwargs.get("pk")
        
        if self.object.gpsdevice:
            self.object.gpsid = self.object.gpsdevice.devicename            
            gps = gpsdevice.objects.get(pk=self.object.gpsdevice.id)
            gps.asignado = True
            gps.save()
        else:            
            #Del vehiculo
            vehiculo = Vehiculo.objects.get(pk=self.object.id)            
            gpsID = vehiculo.gpsdevice.id
            # De gpsdevice 
            gps = gpsdevice.objects.get(pk=gpsID)                  
            gps.asignado = False
            gps.save()
            
            self.object.gpsid = None
        
        form.save()
        return super().form_valid(form)    

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context

class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    success_url = reverse_lazy('administrador:vehiculo_list')
    template_name = 'administrador/ddmanagement/vehiculos/vehiculo_confirm_delete.html'
    
    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        vehiculo = Vehiculo.objects.get(pk=self.object.id)            
        gpsID = vehiculo.gpsdevice.id
        # De gpsdevice 
        gps = gpsdevice.objects.get(pk=gpsID)                  
        gps.asignado = False
        gps.save()
        return super(VehiculoDeleteView, self).delete(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list
        return context