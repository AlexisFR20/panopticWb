from django import forms
from .models import Encuesta, Pregunta, Papeleta, Respuesta, Recomendacion

class EncuestaForm(forms.ModelForm):

    class Meta:
        model = Encuesta
        fields = ["nombre", "categoria"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}), 
        }

class PreguntaForm(forms.ModelForm):

    class Meta:
        model = Pregunta
        fields = ["pregunta", "valor", "orden"]
        widgets = {
            "pregunta": forms.TextInput(attrs={"class": "form-control"}),
            "valor": forms.NumberInput(attrs={"class": "form-control", "step": 1}),
            "orden": forms.NumberInput(attrs={"class": "form-control", "step": 1}),
        }

class PapeletaForm(forms.ModelForm):
    
    class Meta:
        model = Papeleta
        fields = ["planta"]

class RecomendacionForm(forms.ModelForm):

    class Meta:
        model = Recomendacion
        fields = ["papeleta", "nombre", "descripcion", "ponderacion", "vulnerabilidad", "costo", "fecha_compromiso"]
        
        
