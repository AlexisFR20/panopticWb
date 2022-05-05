from core.models import Cliente
from cporte.models import PorteCliente
from cporte.forms import PorteClienteForm
from django.views.generic.list import ListView
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.forms import ClienteForm
from django.urls import reverse, reverse_lazy

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

class ClienteListView(ListView):
    model = Cliente    
    template_name = 'administrador/perfiles_clientes/clientes_list.html'   
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context 
    
class ClienteDetailView(DetailView):
    model = Cliente    
    template_name = 'administrador/perfiles_clientes/clientes_detail.html' 
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class ClienteUpdateView(UpdateView):
    model = Cliente    
    form_class = ClienteForm        
    template_name_suffix = '_update_form'
    template_name = 'administrador/perfiles_clientes/clientes_update_form.html'    
    
    def get_success_url(self):
        return reverse_lazy('administrador:cliente_update', args=[self.object.id]) + '?OK'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
    
class ClienteCreateView(CreateView):
    model = Cliente        
    form_class = ClienteForm 
    template_name = 'administrador/perfiles_clientes/clientes_form.html'    
    
    def get_success_url(self, *args, **kwargs):   
        return reverse('administrador:cliente_list')

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

class ClienteDelete(DeleteView):
    model = Cliente        
    template_name = 'administrador/perfiles_clientes/clientes_confirm_delete.html'    
    success_url =  reverse_lazy('administrador:cliente_list')  
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context

class PorteClienteCreateView(CreateView):
    model = PorteCliente
    template_name = "administrador/perfiles_clientes/porte_clientes_form.html"
    form_class = PorteClienteForm

    def get_success_url(self, *args, **kwargs):    
        messages.add_message(self.request,  messages.SUCCESS, 'Cliente creado exitosamente!')       
        return reverse('administrador:porte_cliente_create')

    def form_valid(self, form, **kwargs):       
        form = form.save(commit=False)        
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books        
        context['css_list'] = css_list
        context['js_list'] = js_list        

        return context
        
