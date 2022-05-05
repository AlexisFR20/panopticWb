from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Incidente, Alarma

class IncidenteForm(forms.ModelForm):

    class Meta:
        model = Incidente
        fields = ["tipo", "cantidad", "fecha", "direccion", "ciudad", "estado", "pais", "lat", "lng", "url_noticia"]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "fecha": forms.SelectDateWidget(attrs={"class": "form-control"}, empty_label=("Año", "Mes", "Día")),
            "direccion": forms.TextInput(attrs={"class": "form-control"}),
            "ciudad": forms.TextInput(attrs={"class": "form-control"}),
            "estado": forms.TextInput(attrs={"class": "form-control"}),
            "pais": forms.TextInput(attrs={"class": "form-control"}),
            "lat": forms.NumberInput(attrs={"class": "form-control"}),
            "lng": forms.NumberInput(attrs={"class": "form-control"}),
            "url_noticia": forms.TextInput(attrs={"class": "form-control"}),
        }

class AlarmaForm(forms.ModelForm):

    class Meta:
        model = Alarma
        fields = ["nombre", "url", "fecha_inicio",]
        widgets = {
            "nombre": forms.TextInput(attrs        = {"class": "form-control"}),
            "url"   : forms.TextInput(attrs        = {"class": "form-control"}),
            "fecha" : forms.SelectDateWidget(attrs = {"class": "form-control"}, empty_label=("Año", "Mes", "Día"))           
        }