from django import forms
from .models import *
from core.models import *

class TipoVehiculoForm(forms.ModelForm):
    class Meta:
        model = TipoVehiculo
        fields = [
            'nombre', 
            'descripcion'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre' }),             
            'descripcion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Descripción' }),             
        }
        labels = {
            'nombre': 'Nombre', 
            'descripcion': 'Descripción',           
        }

class CajaForm(forms.ModelForm):

    class Meta:
        model = Caja
        fields = [
            'identificador',
            'capacidad',
            'tipo',
            'caja_no',
            'caja_placas',
            'cajaeco',
            'sellocaja'
        ]
        widgets = {
            "identificador": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Escriba un alias'}),
            "capacidad": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Indique la capacidad por favor'}),
            "tipo": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Tipo de caja'}),
            "caja_no": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Escriba el número de caja'}),
            "caja_placas": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Escriba el número de placas de caja'}),
            "cajaeco": forms.TextInput(attrs={"class": "form-control", 'placeholder': ''}),
            "sellocaja": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Si lo requiere, indíquelo por favor '}),
        }
        labels = {                        
            'identificador': 'Identificador',
            'capacidad': 'Capacidad',
            'tipo': 'Tipo',
            'caja_no': 'No. de caja',
            'caja_placas': 'Placas de caja',
            'cajaeco': 'No. Económico de caja',
            'sellocaja': 'Sello extra/interior en caja'
        } 


class MovimientoForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)           
        super (MovimientoForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['chofer'].queryset = User.objects.filter(role__alias_rol='chofer').all()
        self.fields['relevo'].queryset = User.objects.filter(role__alias_rol='chofer').all()        
        if self.request != None and self.request.user.role.alias_rol!='administrador':            
            self.fields['vehiculo'].queryset = Vehiculo.objects.filter(disponible=True).filter(gpsdevice__cliente=self.request.user.cliente).all()               
            #self.fields['vehiculo'].queryset = Vehiculo.objects.filter(disponible=True).all()               

    class Meta:
        model = Movimiento
        fields = [            
            "estatus",
            "nombre",
            "tipo_incidente",
            "planta", 
            "chofer",
            "relevo",
            "vehiculo",    
            "emp_transp",        
            "infocarga",
            "doc_completa", 
            "origen", 
            "destino", 
            "origen_coords", 
            "destino_coords", 
            "waypoints",
            "remolque",
            "n_sello",
            "tipo_movimiento", 
            "tiempo_estimado", 
            "tiempo_estimado_google", 
            "fecha_fin",
            "confirmacion",
            "ef",
            "valor_carga", 
            "peso", 
            "chofer", 
            "gls", 
            "lts", 
            "puente", 
            "peaje"]

        widgets = {            
            "estatus": forms.Select(attrs={"class": "form-control"}),   
            "nombre": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Identifique el movimiento'}),
            "tipo_incidente": forms.Select(attrs={"class": "form-control"}),   
            "planta": forms.Select(attrs={"class": "form-control"}),
            "chofer": forms.Select(attrs={"class": "form-control"}),
            "relevo": forms.Select(attrs={"class": "form-control"}),
            "vehiculo": forms.Select(attrs={"class": "form-control"}),            
            "emp_transp": forms.Select(attrs={"class": "form-control"}),            
            "infocarga": forms.TextInput(attrs={"class": "form-control"}),
            "doc_completa": forms.CheckboxInput(attrs={"class": "form-control checkformdj"}),
            "origen": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Introduza la ubicación del orígen'}),
            "destino": forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Introduzca la ubicación del destino'}),
             "origen_coords": forms.TextInput(attrs={"class": "form-control escondido", "readonly": "readonly"}),
            "destino_coords": forms.TextInput(attrs={"class": "form-control escondido", "readonly": "readonly"}),   
            "waypoints": forms.Textarea(attrs={"class": "form-control escondido", "rows": "2"}),            
            "remolque": forms.TextInput(attrs={"class": "form-control"}),
            "n_sello": forms.TextInput(attrs={"class": "form-control"}),
            "tipo_movimiento": forms.TextInput(attrs={"class": "form-control"}),
            "tiempo_estimado": forms.TextInput(attrs={"class": "form-control", 'placeholder': '(En minutos)'}),
            "tiempo_estimado_google": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly" }),
            "fecha_fin": forms.DateTimeInput(attrs={'class': 'form-control escondido'}),
            "confirmacion": forms.CheckboxInput(attrs={'disabled': True, 'class': 'form-control escondido'}),
            "ef": forms.CheckboxInput(attrs={'class': 'form-control escondido'}),
            "valor_carga": forms.TextInput(attrs={"class": "form-control"}),
            "peso": forms.TextInput(attrs={"class": "form-control"}),            
            "gls": forms.NumberInput(attrs={"class": "form-control"}),
            "lts": forms.NumberInput(attrs={"class": "form-control"}),
            "puente": forms.CheckboxInput(attrs={"class": "form-control checkformdj"}),
            "peaje": forms.NumberInput(attrs={"class": "form-control"}), 
        }
        
        labels = {            
            'estatus': 'Estatus',
            'nombre': 'Nombre/Alias',
            'tipo_incidente': 'Tipo de Incidente',
            'planta': 'Unidad de Negocio',
            'chofer': 'Chofer',
            'relevo': 'Relevo',
            'vehiculo': 'Vehículo',
            'emp_transp': 'Empresa Transportista',
            'infocarga': 'Información de la carga',
            'doc_completa': '¿Documentación Completa?',
            'origen': 'Orígen',
            'destino': 'Destino',
            'origen_coords': 'Orígen Coords.',
            'destino_coords': 'Destino Coords.',          
            'remolque': 'Remolque',
            'n_sello': 'Sello',
            'tipo_movimiento': 'Tipo de Movimiento',
            'tiempo_estimado': 'Tiempo Estimado',
            'tiempo_estimado_google': 'Tiempo Estimado Google',
            'fecha_fin': 'Fecha Fin', 
            'confirmacion': 'Confirmar movimiento terminado por chofer', 
            'ef': '¿Movimiento Finalizado?',
            'valor_carga': 'Valor de Carga',
            'peso': 'Peso',
            'chofer': 'Chofer',
            'gls': 'GLS',
            'lts': 'LTS',
            'puente': 'Puente',
            'peaje': 'Peaje'
        }
        
class VehiculoForm(forms.ModelForm):
    
    class Meta:
        model = Vehiculo
        
        fields = [
            "placas",
            "economico",
            "tipo_vehiculo",
            "marca",
            "modelo",
            "anio",
            "seria",
            "gpsdevice",
            "disponible"
        ]

        widgets = {
            "placas" : forms.TextInput(attrs={"class": "form-control"}),
            "economico" : forms.TextInput(attrs={"class": "form-control"}),
            "tipo_vehiculo": forms.Select(attrs={"class": "form-control"}),
            "marca": forms.TextInput(attrs={"class": "form-control"}),
            "modelo": forms.TextInput(attrs={"class": "form-control"}),
            "anio": forms.TextInput(attrs={"class": "form-control"}),
            "seria": forms.TextInput(attrs={"class": "form-control"}),            
            'gpsdevice': forms.Select(attrs={"class": "form-control"}),
            "disponible": forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj'})
        }
        
        labels = {
            'placas': 'Placas',
            'economico': 'No. Económico',
            'tipo_vehiculo': 'Tipo de Vehículo',
            'marca': 'ESN',
            'modelo': 'Modelo',
            'anio': 'Año',
            'seria': 'No. Serie',
            'gpsdevice': 'GPS Asignado',
            'disponible':'¿Disponible?'
        }
        
class GpsDevicesForm(forms.ModelForm):
    
    class Meta:
        model = gpsdevice
        fields = ['cliente', 'deviceid', 'devicename', 'deviceesn',  'activo', 'asignado']
        
        widgets = {
            'cliente': forms.Select(attrs={"class": "form-control"}),             
            'deviceid': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese el ID del dispositivo' }), 
            'devicename': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese el nombre del dispositivo' }), 
            'deviceesn': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese el ESN del dispositivo' }), 
            'activo': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj'}),         
            'asignado': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj'})            
        }
        
        labels = {
            'deviceid': 'GPS Id',
            'devicename': 'Nombre',
            'deviceesn': 'ESN',
            'activo': '¿Activo?',
            'asignado': '¿Se encuentra asignado?',
        }

class CargasForm(forms.ModelForm):
    class Meta:
        model = Carga
        fields = [
            'tipo', 
            'folio',
            'peso',
            'movimiento',
        ]
        widgets = {
            'tipo': forms.Select(attrs={"class": "form-control"}),             
            'folio': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Folio' }),             
            'peso': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Peso de la Carga' }),             
            'movimiento': forms.Select(attrs={"class": "form-control"}),        
        }
        labels = {
            'tipo': 'Tipo de Carga', 
            'folio': 'Folio',
            'peso': 'Peso de la Carga',
            'movimiento': 'Movimiento',           
        }

class ChoferForm(forms.ModelForm):
    
    # def __init__(self, user, *args,**kwargs):
    #     super (ChoferForm,self ).__init__(*args,**kwargs) # populates the post
    #     self.user = User.objects.filter(user.getRolU=='chofer')
    
    class Meta:
        model = User
        fields = ['no_orden', 'first_name', 'last_name',  'tel_pral', 'edad', 'transportista']
        widgets = {
            'no_orden': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Identificación del Empleado' }), 
            'first_name': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba su(s) nombre(s)' }),                        
            'last_name': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba su(s) apellido(s)' }),                        
            'tel_pral': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Agregue un teléfono válido' }),
            'edad': forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese edad real' }),                        
            'transportista': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba la razón social o nombre de la empresa' })    
        }
        
        labels = {               
            'no_orden': 'No. Empleado / Orden', 
            'first_name': 'Nombre',                        
            'last_name': 'Apellido',                        
            'tel_pral': 'Teléfono',
            'edad': 'Edad',                        
            'transportista': 'Empresa Transportista'    
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = [
            'nombre',
            'empresa',
            'email',
            'telefono',
            'domicilio',
            'razon_social',
            'imagen_logo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre' }),             
            'empresa': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Empresa' }),
            'email': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Correo Electronico' }),
            'telefono': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Te;efono' }),
            'domicilio': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Domicilio' }),
            'razon_social': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Razon Social' }),
            
        }
        labels = {
            'nombre': 'Nombre',
            'empresa': 'Empresa',
            'email': 'Correo Electronico',
            'telefono': 'Telefono',
            'domicilio': 'Domicilio',
            'razon_social': 'Razon Social',
            'imagen_logo': 'Imagen Logo'
        }

