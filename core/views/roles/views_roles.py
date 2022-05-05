from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from  core.forms import RoleForm

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_datetimepicker']

class RoleListView(ListView):
    model = Role
    template_name = 'administrador/roles/role_list.html'       
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class RoleDetailView(DetailView):
    model = Role   
    template_name = 'administrador/roles/role_detail.html' 
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class RoleUpdateView(UpdateView):
    model = Role   
    form_class = RoleForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/roles/role_update_form.html'            
    
    def get_success_url(self):        
        return reverse_lazy('administrador:role_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)                
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class RoleCreateView(CreateView):
    model = Role       
    form_class = RoleForm 
    template_name = 'administrador/roles/role_form.html'          
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:role_list')
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class RoleDelete(DeleteView):
    model = Role       
    template_name = 'administrador/roles/role_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:role_list')  
    
    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context