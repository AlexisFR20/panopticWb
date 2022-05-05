from django.contrib import admin
from .models import Categoria_Encuesta, Encuesta, Pregunta, Papeleta, Respuesta

# Register your models here.

class EncuestaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria")

class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("encuesta", "pregunta", "orden")

class PapeletaAdmin(admin.ModelAdmin):
    list_display = ("fecha", "user_aguilas", "encuesta")

admin.site.register(Categoria_Encuesta)
admin.site.register(Encuesta, EncuestaAdmin)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(Papeleta, PapeletaAdmin)
admin.site.register(Respuesta)
#admin.site.register(Analisis)
