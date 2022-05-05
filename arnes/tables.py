import django_tables2 as tables
from django_tables2.utils import A
from .models import Encuesta, Pregunta, Papeleta, Respuesta

class EncuestaTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")
    Detalles = tables.LinkColumn("arnes:detail_encuesta", text="Detalles", args=[A("pk")], attrs={'a': {'class': 'btn btn-info'}}, orderable=False)
    Editar = tables.LinkColumn("arnes:update_encuesta", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)
    Borrar = tables.LinkColumn("arnes:delete_encuesta", text="Borrar", args=[A("pk")], attrs={'a': {'class': 'btn btn-danger'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Encuesta
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "nombre")
    
    def renderActions():
        return "<a href='#' class='btn btn-primary'>Editar</a>"

class PreguntaTable(tables.Table):

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Pregunta
        template_name = "django_tables2/bootstrap4.html"
        fields = ("pregunta", "orden")

class PapeletaTable(tables.Table):

    Detalles = tables.LinkColumn("arnes:detail_papeleta", text="Detalles", args=[A("pk")], attrs={'a': {'class': 'btn btn-info'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Papeleta
        template_name = "django_tables2/bootstrap4.html"
        fields = ("fecha", "planta", "user_aguilas", "encuesta")

class RespuestaTable(tables.Table):

    respuesta = tables.Column()

    def render_repuesta(self):
        return "Si"

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Respuesta
        template_name = "django_tables2/bootstrap4.html"
        fields = ("pregunta_text", "repuesta", "cumple", "ocurrencia", "impacto", "resultado", "observacion")
        