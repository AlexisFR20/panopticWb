import django_tables2 as tables
from django_tables2.utils import A
from .models import Incidente, Alarma

class IncidenteTable(tables.Table):
    tipo = tables.Column(attrs={"th": {"id": "foo"}}, verbose_name="Tipo de incidente")
    direccion = tables.Column(verbose_name="Dirección")
    url_noticia = tables.Column(verbose_name="Noticia")
    Editar = tables.LinkColumn("entorno:update", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)
    Borrar = tables.LinkColumn("entorno:delete", text="Borrar", args=[A("pk")], attrs={'a': {'class': 'btn btn-danger'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Incidente
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "tipo", "fecha", "direccion", "ciudad", "estado", "pais", "lat", "lng", "url_noticia")

    
    def renderActions():
        return "<a href='#' class='btn btn-primary'>Editar</a>"


class AlarmaTable(tables.Table):
    nombre = tables.Column(verbose_name="Nombre")    
    url    = tables.Column(verbose_name="URL Noticia")
    fecha  = tables.Column(verbose_name="Fecha")
    #Editar = tables.LinkColumn("entorno:update", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)
    #Borrar = tables.LinkColumn("entorno:delete", text="Borrar", args=[A("pk")], attrs={'a': {'class': 'btn btn-danger'}}, orderable=False)

    def render_name(self):
        return format_html("<b>{} {}</b>")

    class Meta:
        model = Alarma
        template_name = "django_tables2/bootstrap4.html"
        fields = ("nombre", "url", "fecha")

    
    def renderActions():
        return "<a href='#' class='btn btn-primary'>Editar</a>"
        
        