from django import forms
from .models import *
import requests
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
import facturama
import tempfile, os

class PorteClienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PorteClienteForm, self).__init__(*args, **kwargs)
        info = {'Authorization':'Basic aW9ueWh6OmZlbmRlcmpwNjAwMTA='}
        permisos = requests.get('https://apisandbox.facturama.mx/api/catalogs/cartaporte/TipoPermiso',headers=info).json()
        PERMISOS_CHOICES = []
        for p in permisos:
            PERMISOS_CHOICES.append((p["Clave"], p["Descripcion"]))
        self.fields["tipoPermiso"].choices = PERMISOS_CHOICES

    REGIMEN_CHOICES = [
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
    ]

    tipoPermiso = forms.ChoiceField(widget=forms.Select(attrs = { 'class': 'form-control'}), initial="",required=True)
    regimen_fiscal = forms.ChoiceField(widget=forms.Select(attrs = { 'class': 'form-control'}),choices = REGIMEN_CHOICES, initial="",required=True)
    cer = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['cer'])])
    key = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['key'])])
    privateKey = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "type": "password",'placeholder': 'Contraseña'}),
    label="Contraseña del certificado")

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
            "numPermiso": forms.TextInput(attrs={"class": "form-control", "placeholder": "NumPermSct"})
        }

        labels = {
            "nombre": "Nombre del cliente",
            "path_img":"Logo factura"
        }
    
    def clean(self):
        facturama._credentials = ("ionyhz","fenderjp60010")
        facturama.sandbox = True
    
        cleaned_data = super().clean() 

        file_key = cleaned_data.get("key")
        file_cer = cleaned_data.get("cer")
        tmp_key = tempfile.NamedTemporaryFile(delete=False)
        tmp_cer = tempfile.NamedTemporaryFile(delete=False)

        with open(tmp_key.name, "wb") as f:
            f.write(file_key.read())

        with open(tmp_cer.name, "wb") as f:
            f.write(file_cer.read())

        try:
            facturama.csdsMultiEmisor.upload(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("privateKey"))
        except Exception as e:
            print(e)
            raise ValidationError("Error al cargar csds")
        finally:
            os.remove(tmp_key.name)
            os.remove(tmp_cer.name)
            
        return cleaned_data

class PorteReceiverForm(forms.ModelForm):

    """
    def __init__(self, type, *args, **kwargs):
        super(PorteReceiverForm, self).__init__(*args,**kwargs)
        self.type = type
    """

    class Meta:
        model = PorteReceiver
        fields =  ["nombre","rfc","razon_social","calle","exterior","interior","colonia","cp","localidad","municipio","estado","pais"]

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
            "pais": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pais'})
        }

        labels = {
            "nombre": "Nombre del cliente",
            "cp": "Código Postal",
            "pais": "País"
        }
    
    """
    #Ya no se usa, dado que ya no se comunica con facturama.
    def clean(self):
        
        facturama._credentials = ("ionyhz","fenderjp60010")
        facturama.sandbox = True
    
        cleaned_data = super().clean() 
         
        file_key = cleaned_data.get("key")
        file_cer = cleaned_data.get("cer")
        tmp_key = tempfile.NamedTemporaryFile(delete=False)
        tmp_cer = tempfile.NamedTemporaryFile(delete=False)

        with open(tmp_key.name, "wb") as f:
            f.write(file_key.read())

        with open(tmp_cer.name, "wb") as f:
            f.write(file_cer.read())

        try:
            if self.type == "update":
                facturama.csdsMultiEmisor.update(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("privateKey"))
            elif self.type == "create":
                facturama.csdsMultiEmisor.upload(cleaned_data.get("rfc"),tmp_key.name,tmp_cer.name,cleaned_data.get("privateKey"))
        except Exception as e:
            print(e)
            raise ValidationError("Error al cargar csds")
        finally:
            os.remove(tmp_key.name)
            os.remove(tmp_cer.name)
            
        return cleaned_data
        """
