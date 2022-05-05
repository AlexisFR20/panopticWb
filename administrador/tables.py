import django_tables2 as tables
from django_tables2.utils import A
from simplejson import OrderedDict
from arnes.models import Encuesta, Pregunta, Papeleta, Respuesta, Categoria_Encuesta
import itertools
counter = itertools.count() 

class EncuestaTable(tables.Table):
    counter = tables.TemplateColumn('{{ row_counter|add:1 }}', verbose_name='#')
    nombre = tables.Column(verbose_name="Nombre")
    Detalles = tables.LinkColumn("administrador:admin_detail_encuesta", text="Detalles", args=[A("pk")], attrs={'a': {'class': 'btn btn-info'}}, orderable=False)
    Editar = tables.LinkColumn("administrador:admin_update_encuesta", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)
    Borrar = tables.LinkColumn("administrador:admin_delete_encuesta", text="Borrar", args=[A("pk")], attrs={'a': {'class': 'btn btn-danger'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Encuesta
        template_name = "django_tables2/bootstrap4.html"
        fields = ["counter", "nombre"]
    
    def renderActions():
        return "<a href='#' class='btn btn-primary'>Editar</a>"

"""
class AnalisisTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")
    Editar = tables.LinkColumn("administrador:admin_update_analisis", text="Editar", args=[A("pk")], attrs={"a": {"class": "btn btn-primary"}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Analisis
        template_name = "django_tables2/bootstrap4.html"
        fields = ["nombre"]
"""

class CategoriaTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")
    Editar = tables.LinkColumn("administrador:admin_update_categoria", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Categoria_Encuesta
        template_name = "django_tables2/bootstrap4.html"
        fields = ["nombre"]


class PreguntaTable(tables.Table):

    Editar = tables.LinkColumn("administrador:admin_edit_pregunta", text="Editar", args=[A("encuesta_id"), A("id")], attrs={'a': {'class': 'btn btn-edit'}}, orderable=False)
    Eliminar = tables.LinkColumn("administrador:admin_delete_pregunta", text="Eliminar", args=[A("encuesta_id"), A("id")], attrs={'a': {'class': 'btn btn-delete'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Pregunta
        template_name = "django_tables2/bootstrap4.html"
        fields = ("pregunta", "valor", "orden")

class PapeletaTable(tables.Table):

    Detalles = tables.LinkColumn("administrador:admin_detail_papeleta", text="Detalles", args=[A("pk")], attrs={'a': {'class': 'btn btn-info'}}, orderable=False)

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
        