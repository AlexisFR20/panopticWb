from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ddmanagement.forms import ChoferForm
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' , 'js_datetimepicker']

#Vistas de Registro de Paquetería
class ChoferListView(ListView):
    model = User
    template_name = 'administrador/ddmanagement/choferes/chofer_list.html'   
    
    # def dispatch(self):                
    #     return self.model.objects.filter(role__alias_rol="chofer")
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class ChoferDetailView(DetailView):
    model = User    
    template_name = 'administrador/ddmanagement/choferes/chofer_detail.html' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class ChoferUpdateView(UpdateView):
    model = User    
    form_class = ChoferForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/ddmanagement/choferes/chofer_update_form.html'        
    
    def dispatch(self, request, *args, **kwargs):        
        PK = self.kwargs['pk']
        user = get_object_or_404(User, id=PK)               
        if user.role.alias_rol != 'chofer':
             return redirect('administrador:chofer_list')
        
        context =super(ChoferUpdateView, self).dispatch(request, *args, **kwargs)
        context['css_list'] = css_list
        context['js_list'] = js_list    
                                        
        return context
    
    def get_success_url(self):
        # print('ID EN UPDATE SUBMIT')
        # print(self.object.id)
        return reverse_lazy('administrador:chofer_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)        
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class ChoferCreateView(CreateView):
    model = User        
    form_class = ChoferForm 
    template_name = 'administrador/ddmanagement/choferes/chofer_form.html'          
    
    def get_success_url(self, *args, **kwargs):        
        return reverse('administrador:chofer_list')

    def form_valid(self, form, **kwargs):
        
        form = form.save(commit=False)        
        form.username = slugify(form.first_name+form.last_name+str(form.edad))
        form.role = get_object_or_404(Role, nombre='CHOFER')   
        print( self.kwargs )
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class ChoferDelete(DeleteView):
    model = User        
    template_name = 'administrador/ddmanagement/choferes/chofer_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:chofer_list')  
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context