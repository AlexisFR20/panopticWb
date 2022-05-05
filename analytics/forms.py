from django import forms
from .models import *
from core.models import Planta
from analytics.models import Paqueteria, Concentracion, Logro

class RondinForm(forms.ModelForm):

    class Meta:
        model = Rondin
        fields = ["cliente", "planta", "categoria", "nombre", "tiempo_estimado", "correos_contacto"]
        widgets = {
            "cliente": forms.Select(attrs={"class": "form-control"}),
            "planta": forms.Select(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tiempo_estimado": forms.NumberInput(attrs={"class": "form-control", "step": "1"}),
            "correos_contacto": forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
        }


class PuntoForm(forms.ModelForm):

    class Meta:
        model = Punto
        fields = ["nombre", "tareas"]
        widgets = {
            "rondin": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "tareas": forms.Textarea(attrs={"class": "form-control"}),
        }

class F_VisitanteForm(forms.ModelForm):

    class Meta:
        model = F_Visitantes
        fields = [
            'planta',
            'tipo',
            'nombre',
            'empresa',
            'anfitrion',
            'confirmo_anfitrion',
            'identificacion',
            'gafete',
            'placas',
            'entrada',
            'salida'
        ]
        widgets = {
            'planta': forms.Select(attrs={ 'class': 'form-control' }),
            'tipo': forms.Select(attrs={ 'class': 'form-control' }),
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo' }),
            'empresa': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre de la empresa' }),
            'anfitrion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo del Anfitrion' }),
            'confirmo_anfitrion': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj ', 'placeholder': 'Nombre completo' }),
            'identificacion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Identificacion' }),
            'gafete': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Gafete' }),            
            'placas': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Placas' }),            
            'entrada': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Fecha de Entrada' }),
            'salida': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Fecha de Salida' }),            
        }
        labels = {
            'planta': 'Unidad de Negocio',
            'tipo': 'Tipo de Visitante',
            'nombre': 'Nombre Completo',
            'empresa': 'Nombre de la Empresa',
            'anfitrion': 'Nombre del Anfitrion',
            'confirmo_anfitrion': 'Confirmar Anfitrion',
            'identificacion': 'Identificacion',
            'gafete': 'Gafete',
            'entrada': 'Fecha de Entrada',
            'salida': 'Fecha de Salida',
        }

class PaqueteriaForm(forms.ModelForm):
    
    class Meta:
        model = Paqueteria
        fields = ['guia','nombre', 'empresa', 'nota',  'destinatario', 'user_aguilas']
        widgets = {
            'guia': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Número de Guía' }),
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo' }), 
            'empresa': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre / Razón Social' }),            
            #'fecha': forms.DateTimeInput(attrs={ 'class': 'form-control' }),
            'nota': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'Escriba sus observacones relevantes' }),
            'destinatario': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre / Departamento'}),
            'user_aguilas': forms.Select(attrs={ 'class': 'form-control' }),
            #'un': forms.Select(attrs={ 'class': 'form-control' })
        }
        labels = {
            'guia': 'Guía',
            'nombre': 'Nombre de quien entrega paquete',
            'empresa': 'Empresa de Orígen',
            #'fecha': 'Fecha de Recibido',
            'nota': 'Observaciones',
            'destinatario': 'Destinatario',
            'user_aguilas': 'Guardia',
            #'un':  'Unidad de Negocio / Planta'
        }

class Categoria_CursoForm(forms.ModelForm):
    class Meta:
        model = Categoria_Curso
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo' }),             
        }
        labels = {
            'nombre': 'Nombre de la Categoría',            
        }

class GradoForm(forms.ModelForm):
    
    class Meta:
        model = Grado
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo' }),             
        }
        labels = {
            'nombre': 'Nombre del Grado',            
        }

class CursoForm(forms.ModelForm):
    
    class Meta:
        model = Curso
        fields = [
            'nombre',
            'grado',
            'categoria'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre completo' }),
            'grado': forms.Select(attrs={ 'class': 'form-control' }),
            'categoria': forms.Select(attrs={ 'class': 'form-control' }),                         
        }
        labels = {
            'nombre': 'Nombre del Curso', 
            'grado': 'Nombre del Grado',
            'categoria': 'Categoría del Curso',           
        }


class ConcentracionForm(forms.ModelForm):
    
    class Meta:
        model = Concentracion
        fields = [
            'no_orden',
            'calificacion',
            'fecha_aplicacion',
            'veces_aplicados',
            'tiempo_dedicado',
            'user_aguilas',
            'puesto',
            'cliente',
            'sitio',
            'curso',
            'grado',
            'categoria'
        ]
        widgets = {
            'no_orden': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'No. Orden' }), 
            'calificacion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Calificación' }),
            'fecha_aplicacion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Fecha de Aplicación' }),            
            'veces_aplicados': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Veces Aplicado' }),
            'tiempo_dedicado': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Tiempo Dedicado'}),
            'user_aguilas': forms.Select(attrs={ 'class': 'form-control' }),
            'puesto': forms.Select(attrs={ 'class': 'form-control' }),
            'cliente': forms.Select(attrs={ 'class': 'form-control'}),
            'sitio': forms.Select(attrs={ 'class': 'form-control'}),
            'curso': forms.Select(attrs={ 'class': 'form-control' }),
            'grado': forms.Select(attrs={ 'class': 'form-control' }),
            'categoria': forms.Select(attrs={ 'class': 'form-control' }),
        }
        labels = {
            'no_orden': 'No. Orden', 
            'calificacion': 'Calificación',
            'fecha_aplicacion': 'Fecha de Aplicación',            
            'veces_aplicados': 'Veces Aplicado',
            'tiempo_dedicado': 'Tiempo Dedicado',
            'user_aguilas': 'Aguilas',
            'puesto': 'Puesto',
            'cliente': 'Cliente',
            'sitio': 'Sitio',
            'curso': 'Curso',
            'grado': 'Grado',
            'categoria': 'Categoria',
        }

class EmpleadosgForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        super (EmpleadosgForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['user_aguilas'].queryset = User.objects.filter(role__alias_rol="guardia")      
    
    class Meta:
        model = Empleado_Sin_Gafete
        fields = ['empleado', 'bolgafetepersonal', 'bolgafetevehicular',  'no_emp', 'departamento', 'jefe', 'fecha', 'fecha_salida', 'turno',  'motivo', 'planta', 'user_aguilas']
        widgets = {
            'empleado': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre Completo' }),            
            'bolgafetepersonal': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj'}),
            'bolgafetevehicular': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj'}),
            'no_emp': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Identificación del Empleado' }), 
            'departamento': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba el Departamento que corresponda' }),            
            'jefe': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre de su Jefe Inmediato' }),    
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control'}),        
            'turno': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Primario / Secundario' }),            
            'motivo': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'Escriba la razón por la cual el empleado no trajo su gafete' }  ),
            'planta': forms.Select(attrs={ 'class': 'form-control' }),       
            'user_aguilas': forms.Select(attrs={ 'class': 'form-control' })            
        }
        
        labels = {               
            'jefe': 'Supervisor',
            'planta': 'Unidad de Negocio',
            'user_aguilas': 'Guardia',            
        }

class AreaRestringidaForm(forms.ModelForm):
    
    def __init__(self, *args,**kwargs):
        super (AreaRestringidaForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['user_aguilas'].queryset = User.objects.filter(role__alias_rol="guardia")      
    
    class Meta:
        model = Area_Restringida
        fields = ['no_emp', 'nombre', 'departamento', 'fecha', 'fecha_salida', 'anfitrion', 'tiempo', 'nota', 'planta', 'user_aguilas']
        widgets = {            
            'no_emp': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'No. de Empleado / No. Gafete' }),                    
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre Completo' }),                    
            'departamento': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba el departamento al que pertenece.' }),    
            'fecha': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'fecha_salida': forms.DateTimeInput(attrs={'class': 'form-control'}),                        
            'anfitrion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre de quien autorizó' }),                        
            'tiempo': forms.Select(attrs={ 'class': 'form-control', 'placeholder': 'Tiempo' }),            
            'nota': forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': 'Escriba sus notas / observaciones' }),
            'planta': forms.Select(attrs={ 'class': 'form-control' }),       
            'user_aguilas': forms.Select(attrs={ 'class': 'form-control' })            
        }  
        
        labels = {            
            'no_emp': 'No. Emp.',
            'nombre': 'Nombre Completo',
            'departamento': 'Departamento',
            'fecha': 'Fecha Entrada',
            'fecha_salida': 'Fecha Salida',
            'anfitrion': 'Nombre de quien autorizó',
            'tiempo': 'Tiempo',
            'nota': 'Notas',
            'planta': 'Unidad de Negocio',
            'user_aguilas': 'Guardia',            
        }        
        
class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = [
            'user_aguilas', 
            'planta',
            'fecha',
            'logro',
            'accion',
            'estatus',
            'observaciones'
        ]
        
        widgets = {
            'user_aguilas': forms.Select(attrs={ 'class': 'form-control'}), 
            'planta': forms.Select(attrs={ 'class': 'form-control' }),
            'fecha': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Introduzca una fecha válida' }),  
            'logro': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba el nombre del logro obtenido' }),
            'accion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba la Acción ha realizada' }),
            'estatus': forms.Select(attrs={ 'class': 'form-control' }),
            "observaciones": forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Escriba las Observaciones', "rows": "2"}),   
        }                                
                                         
        labels = {
            'user_aguilas': 'Usuario',
            'planta': 'Unidad de Negocio',
            'fecha': 'Fecha',
            'logro': 'Logro',
            'accion': 'Acción',
            'estatus': 'Estatus',
            'observaciones': 'Observaciones'     
        }

class FaltaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        #self.fields['guardia'].queryset = User.objects.filter(role__alias_rol="guardia")

    class Meta:
        model = Falta
        fields = ["cliente", "planta", "nombre", "fecha", "turno", "motivo"]
        widgets = {
            "cliente": forms.Select(attrs={'class': 'form-control', 'placeholder': 'cliente', 'required': ''}),
            "planta": forms.Select(attrs={'class': 'form-control', 'placeholder': 'planta', 'required': ''}),
            "nombre": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nombre de guardia', 'required': ''}),
            "fecha": forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'fecha', 'required': ''}),
            "turno": forms.Select(attrs={'class': 'form-control', 'placeholder': 'turno', 'required': ''}),
            "motivo": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'motivo'}),
        }
        labels = {
            'nombre': 'Guardia que faltó*',
            "fecha": "Fecha de falta*",
            "cliente": "Cliente*",
            "planta": "Unidad de negocio / Planta*",
            "turno": "Turno*",
            "motivo": "Motivo de la falta",
        }
