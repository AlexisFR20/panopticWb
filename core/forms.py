from django import forms
from .models import *
from core.models import *
from core.utils import *
from ddmanagement.models import *
from django.core.exceptions import ValidationError
import facturama
import shutil, tempfile, os, time, base64
from django.core.files.storage import FileSystemStorage

class RoleForm(forms.ModelForm):
    
    class Meta:
        model = Role
        fields = ['nombre', 'alias_rol', 'grupo']
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese nombre del rol' }), 
            'alias_rol': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Ingrese Alias del rol, sin espacios  y en minúsculas' }),                        
            'grupo': forms.Select(attrs={ 'class': 'form-control' }),            
        }
        labels = {
            'nombre': 'Nombre de Rol',
            'alias_rol': 'Alias', 
            'grupo': 'Grupo'            
        }
        
    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        self.fields['grupo'].empty_label = "Selección de grupo"

class PlantaForm(forms.ModelForm):
    
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)           
        super (PlantaForm,self ).__init__(*args,**kwargs)        
        
        if self.request!=None:            
            user = self.request.user            
            planta = self.request.user.planta
            cliente = self.request.user.cliente
            role = self.request.user.role.alias_rol  
            roles = ['ceo', 'administrador']            
            self.fields['cliente'].queryset = getClientesLista(roles, user)             
        
    class Meta:
        model = Planta
        fields = [
            'nombre',
            'alias',
            'foto',
            'tipo',
            'giro',
            #'cinterno',
            'direccion',
            'ciudad',
            'estado',
            'pais',
            'lat', 
            'lng',            
            'slug',          
            'cliente',
            'gradio',
            #'polyradio',
            'sucursal',            
            'estatus_cobertura_estable',
            'estatus_cobertura_relevante',
            'estatus_ausentismo_estable',
            'estatus_ausentismo_relevante',
            'estatus_rotacion_estable',
            'estatus_rotacion_relevante',
            'mails_zona',
            'mails_analisis_riesgo',
            'mails_dd',
            'mails_predictive'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre de la Unidad de Negocio' }),  
            #'foto': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Foto' }),
            'alias': forms.TextInput(attrs={ 'class': 'form-control escondido', 'placeholder': 'Alias' }),
            'tipo': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Describa el tipo / categoría de la empresa' }),
            'giro': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Mencione el giro de trabajo' }),
            #'cinterno': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'CInterno' }),
            'direccion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Escriba una dirección' }),
            'ciudad': forms.TextInput(attrs={ 'class': 'form-control' }),
            'estado': forms.TextInput(attrs={ 'class': 'form-control' }),
            'pais': forms.TextInput(attrs={ 'class': 'form-control'}),
            'lat': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Latitud' }),
            'lng': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Longitud' }),            
            #'status': forms.Select(attrs={ 'class': 'form-control' }),           
            'slug': forms.TextInput(attrs={ 'class': 'form-control escondido' }),
            #'pcapacitacion': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'PCapacitación' }),
            #'pcobertura': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'PCobertura' }),
            'cliente': forms.Select(attrs={ 'class': 'form-control' }),
            'gradio': forms.NumberInput(attrs={ 'class': 'form-control' }),
            #'polyradio': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'PolyRadio' }),
            'sucursal': forms.Select(attrs={ 'class': 'form-control' }),
            'estatus_cobertura_estable': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'estatus_cobertura_relevante': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'estatus_ausentismo_estable': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'estatus_ausentismo_relevante': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'estatus_rotacion_estable': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'estatus_rotacion_relevante': forms.NumberInput(attrs={ 'class': 'form-control' }),
            'mails_zona': forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            'mails_analisis_riesgo': forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            'mails_dd': forms.Textarea(attrs={"class": "form-control", "rows": "2"}),
            'mails_predictive': forms.Textarea(attrs={"class": "form-control", "rows": "2"})
        }
        labels = {
            'nombre': 'Nombre',
            'foto': 'Imagen de la Unidad de Negocio',
            'alias': 'Alias',
            'tipo': 'Tipo',
            'giro': 'Giro',            
            'direccion': 'Dirección',
            'ciudad': 'Ciudad',
            'estado': 'Estado',
            'pais': 'País',
            'lat': 'Latitud',
            'lng': 'Longitud',            
            'status': 'Estatus',
            'slug': 'Slug',            
            'cliente': 'Cliente',
            'gradio': 'Radio Delincuencial',            
            'sucursal': 'Sucursal',
            'estatus_cobertura_estable': 'Criterio de Cobertura Estable (%)',
            'estatus_cobertura_relevante': 'Criterio de Cobertura Relevante (%)',
            'estatus_ausentismo_estable': 'Criterio de Ausentismo Estable (%)',
            'estatus_ausentismo_relevante': 'Criterio de Ausentismo Estable (%)',
            'estatus_rotacion_estable': 'Criterio de Rotación Estable (%)',
            'estatus_rotacion_relevante': 'Criterio de Rotación Estable (%)', 
            'mails_zona': 'Emails para Notificacines en Zona 0',
            'mails_analisis_riesgo': 'Emails para Notificacines en Análisis de Riesgo',
            'mails_dd': 'Emails para Notificacines en D&D Management',
            'mails_predictive': 'Emails para Notificacines en Predictive Analytics'            
        }

class AreapermisoForm(forms.ModelForm):
    class Meta:
        model = Areapermiso
        fields = [
            'nombre', 
            'alias',
            'orden'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre' }),             
            'alias': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Alias' }),             
            'orden': forms.NumberInput(attrs={ 'class': 'form-control', 'placeholder': 'Orden' }),             
        }
        labels = {
            'nombre': 'Nombre', 
            'alias': 'Alias',
            'orden': 'Orden',           
        }

class PermisosForm(forms.ModelForm):
    class Meta:
        model = Permisos
        fields = [
            'nombre', 
            'desc',
            'estado',
            #'role',
            'areapermiso',
            'cliente',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre' }),             
            'desc': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Descripción' }),             
            'estado': forms.CheckboxInput(attrs={ 'class': 'form-control checkformdj' }),             
            #'role': forms.Select(attrs={ 'class': 'form-control', 'placeholder': 'Rol' }),        
            'areapermiso': forms.Select(attrs={ 'class': 'form-control', 'placeholder': 'Área de Permiso' }),             
            'cliente': forms.Select(attrs={ 'class': 'form-control', 'placeholder': 'Cliente' }),             
        }
        labels = {
            'nombre': 'Nombre', 
            'desc': 'Descripción',
            'estado': 'Estado',
            #'role': 'Rol'
            'areapermiso': 'Área de Permiso',
            'cliente': 'Cliente',         
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nombre', 
            'razon_social',
            'domicilio',
            'corporativo',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre' }),             
            'razon_social': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Razon Social' }),             
            'domicilio': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Domicilio' }),          
            'corporativo': forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Corporativo' }),             
        }
        labels = {
            'nombre': 'Nombre', 
            'razon_social': 'Razon Social',
            'domicilio': 'Domicilio',
            'corporativo': 'Corporativo',         
        }

class PorteClienteForm(forms.ModelForm):
    REGIMEN_CHOICES = (
        ("601", "601 - General de Ley Personas Morales"),
        ("603", "603 - Personas Morales con Fines no Lucrativos"),
        ("609", "609 - Consolidación"),
        ("612", "612 - Personas Fisicas con Actividades Empresariales y Profesionales"),
        ("620", "620 - Sociedades Cooperativas de Producción que optan por diferir sus ingresos"),
        ("622", "622 - Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras"),
        ("632", "623 - Opcional para Grupos de Sociedades"),
        ("624", "624 - Coordinados"),
        ("628", "628 - Hidrocarburos"),
        ("607", "607 - Régimen de Enajenación o Adquisición de Bienes")
    )

    regimen_fiscal = forms.ChoiceField(choices = REGIMEN_CHOICES, initial="",required=True)

    class Meta:
        model = PorteCliente
        fields =  "__all__"

        widgets = {
            "nombre": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre'}),
            "rfc": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'RFC'}),
            "razon_social": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Razon Social'}),
            "calle": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle'}),
            "exterior": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Exterior'}),
            "interior": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Interior'}),
            "colonia": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia'}),
            "cp": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C. P.'}),
            "localidad": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            "municipio": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipio'}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            "pais": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais'}),
            "regimen_fiscal": forms.Select(attrs = { 'class': 'form-control'}),
            "path_privateKey": forms.TextInput(attrs = {"type":"password"})
        }

        labels = {
            "nombre": "Nombre del cliente",
            "path_key": "Archivo key",
            "path_cer": "Archivo cer",
            "path_img":"Logo factura",
            "regimen_fiscal": "Regimen Fiscal",
            "path_privateKey": "Contraseña del key"
        }
    
    def clean(self):
        facturama._credentials = ("ionyhz","fenderjp60010")
        facturama.sandbox = True
    
        cleaned_data = super().clean() 

        file_key = cleaned_data.get("path_key")
        file_cer = cleaned_data.get("path_cer")
        tmp_key = tempfile.NamedTemporaryFile(delete=False)
        tmp_cer = tempfile.NamedTemporaryFile(delete=False)

        with open(tmp_key.name, "wb") as f:
            f.write(file_key.read())

        with open(tmp_cer.name, "wb") as f:
            f.write(file_cer.read())

        try:
            facturama.csdsMultiEmisor.upload(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("path_privateKey"))
        except Exception as e:
            print(e)
            raise ValidationError("Error al cargar csds")
        finally:
            os.remove(tmp_key.name)
            os.remove(tmp_cer.name)
            
        return cleaned_data

"""
class PorteReceiverForm(forms.ModelForm):
    def __init__(self, type, *args, **kwargs):
        super(PorteReceiverForm, self).__init__(*args,**kwargs)
        self.type = type

    class Meta:
        model = PorteReceiver
        fields =  ["nombre","rfc","razon_social","calle","exterior","interior","colonia","cp","localidad","municipio","estado","pais","path_key","path_cer","path_privateKey"]

#"calle","exterior","interior","colonia","cp","localidad","municipio","estado","pais"
        widgets = {
            "nombre": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Nombre'}),
            "rfc": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'RFC'}),
            "razon_social": forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': 'Razon Social'}),
            "calle": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Calle'}),
            "exterior": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Exterior'}),
            "interior": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. Interior'}),
            "colonia": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Colonia'}),
            "cp": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'C. P.'}),
            "localidad": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Localidad'}),
            "municipio": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Municipio'}),
            "estado": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            "pais": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais'}),
            "path_privateKey": forms.TextInput(attrs = {"type":"password"})
        }

        labels = {
            "nombre": "Nombre del cliente",
            "cp": "Código Postal",
            "pais": "País",
            "path_key": "Archivo key",
            "path_cer": "Archivo cer",
            "path_privateKey": "Contraseña del key"
        }
    
    def clean(self):

        facturama._credentials = ("ionyhz","fenderjp60010")
        facturama.sandbox = True
    
        cleaned_data = super().clean() 

        file_key = cleaned_data.get("path_key")
        file_cer = cleaned_data.get("path_cer")
        tmp_key = tempfile.NamedTemporaryFile(delete=False)
        tmp_cer = tempfile.NamedTemporaryFile(delete=False)

        with open(tmp_key.name, "wb") as f:
            f.write(file_key.read())

        with open(tmp_cer.name, "wb") as f:
            f.write(file_cer.read())

        try:
            if self.type == "update":
                print("This is update!")
                facturama.csdsMultiEmisor.update(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("path_privateKey"))
            elif self.type == "create":
                facturama.csdsMultiEmisor.upload(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("path_privateKey"))
        except Exception as e:
            print(e)
            raise ValidationError("Error al cargar csds")
        finally:
            os.remove(tmp_key.name)
            os.remove(tmp_cer.name)
            
        return cleaned_data
        """