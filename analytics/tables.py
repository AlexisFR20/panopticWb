import django_tables2 as tables
from django_tables2.utils import A
from .models import Rondin, Punto

class RondinTable(tables.Table):
    puntos = tables.Column(accessor="puntos_count", verbose_name="Puntos")
    Detalles = tables.LinkColumn("analytics:detail_rondin", text="Detalles", args=[A("pk")], attrs={'a': {'class': 'btn btn-info'}}, orderable=False)
    Editar = tables.LinkColumn("analytics:update_rondin", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)
    Borrar = tables.LinkColumn("analytics:delete_rondin", text="Borrar", args=[A("pk")], attrs={'a': {'class': 'btn btn-danger'}}, orderable=False)

    class Meta:
        model = Rondin
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "cliente", "planta", "categoria", "nombre", "tiempo_estimado", "correos_contacto")

    def render_tiempo_estimado(self, value, record):
        return str(value)+" minutos"

class PuntoTable(tables.Table):

    Editar = tables.LinkColumn("analytics:update_punto", text="Editar", args=[A("pk")], attrs={'a': {'class': 'btn btn-primary'}}, orderable=False)

    class Meta:
        model = Punto
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "nombre", "tareas")


        