#from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_Visitantes, F_ES_Trailers, F_18_puntos_Trailer, Incidentes, EntradaEquipo, ItemEntradaEquipo,  ItemEntradaMaterial, EntradaMateriales, EntradaVehiculo, Paqueteria, Empleado_Sin_Gafete, Area_Restringida, RecibosItems, RecibosAlmacen, 
from analytics.models import *
from cporte.models import PorteCarta
from arnes.models import Encuesta, Pregunta, Papeleta, Respuesta
from core.models import User, Cliente, Planta
from ddmanagement.models import * 
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class PuntoSerializer(serializers.ModelSerializer):

	class Meta:
		model = Punto
		fields = ('id', 'nombre', 'tareas')

class RondinSerializer(serializers.ModelSerializer):
	puntos = PuntoSerializer(many=True, source="punto_set")
	cliente = serializers.StringRelatedField()
	planta = serializers.StringRelatedField()

	class Meta:
		model = Rondin
		fields = ['id', 'nombre', 'tiempo_estimado', 'cliente_id', 'planta_id', 'cliente', 'planta', 'puntos' ]

class RondinHechoSerializer(serializers.ModelSerializer):
	rondin = RondinSerializer()

	class Meta:
		model = RondinHecho
		fields = [ 'id', 'guardia', 'hora_inicio', 'hora_fin', 'rondin']

class PuntoHechoSerializer(serializers.ModelSerializer):

	class Meta:
		model = PuntoHecho
		fields = "__all__"

class CajonSerializer(serializers.ModelSerializer):

        class Meta:
                model = Cajon
                fields = "__all__"

class TrasladoSerializer(serializers.ModelSerializer):
        
        class Meta:
                model = PorteCarta
                fields = "__all__"

class PatioSerializer(serializers.ModelSerializer):
        cajones = CajonSerializer(many=True, source="cajon_set")
        planta = serializers.StringRelatedField()

        class Meta:
                model = Patio
                fields = ['id','planta','cajones']


class EvidenciaSerializer(serializers.ModelSerializer):

	class Meta:
		model = EvidenciaPunto
		fields = "__all__"

class LoginUserSerializer(serializers.ModelSerializer):

	token = serializers.SerializerMethodField()
	
	class Meta:
		model = User
		fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_active", "cliente_id", "planta_id", "getRolAlias", "getRolU", "token"]

	def get_token(self, obj):

		try:
			token = Token.objects.get(user_id=obj.id)
		except Token.DoesNotExist:
			token = Token.objects.create(user_id=obj.id)
		return token.key
			
class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_active", "planta_id", "getRolAlias"]

class FVisitantesSerializer(serializers.ModelSerializer):

	class Meta:
		model = F_Visitantes
		fields = "__all__"

class FESTrailersSerializer(serializers.ModelSerializer):

	class Meta:
		model = F_ES_Trailers
		fields = "__all__"

class F18puntosTrailerSerializer(serializers.ModelSerializer):
	class Meta:
		model = F_18_puntos_Trailer
		fields = "__all__"

class IncidentesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Incidentes
		fields = "__all__"

class ItemEntradaEquipoSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ItemEntradaEquipo
		fields = "__all__"

class EntradaEquipoSerializer(serializers.ModelSerializer):
	items = ItemEntradaEquipoSerializer(many=True, source="item")
	class Meta:
		model = EntradaEquipo
		fields = "__all__"
   
class ItemEntradaMaterialesSerializer(serializers.ModelSerializer):
	
  class Meta:
    model = ItemEntradaMaterial
    fields = "__all__"

class EntradaMaterialesSerializer(serializers.ModelSerializer):
  items = ItemEntradaMaterialesSerializer(many=True, source="item")
  class Meta:
    model = EntradaMateriales
    fields = "__all__"
    
class EntradaVehiculoSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = EntradaVehiculo
		fields = "__all__"
   
class PaqueteriaSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Paqueteria
		fields = "__all__"
   
class EmpleadiGafeteSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Empleado_Sin_Gafete
		fields = "__all__"
   
class AreaRestringidaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Area_Restringida
		fields = "__all__"
    
   
class PreguntaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Pregunta
		fields = "__all__"		
   
class EncuestaSerializer(serializers.ModelSerializer):

	categoria = serializers.StringRelatedField()
	preguntas = PreguntaSerializer(many=True, source="pregunta_set")
	class Meta:
		model = Encuesta
		fields = "__all__"



class EncuestaDetalleSerializer(serializers.ModelSerializer):

	categoria = serializers.StringRelatedField()

	class Meta:
		model = Encuesta
		fields = "__all__"
   
class RespuestaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Respuesta
		fields = "__all__"

class PapeletaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Papeleta
		fields = "__all__"
   
class PlantaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Planta
		fields = "__all__"
			

class ClienteSerializer(serializers.ModelSerializer):
	
	plantas = PlantaSerializer(many=True, source="planta_set")

	class Meta:
		model = Cliente
		fields = "__all__"
   
class RecibosItemsSerializer(serializers.ModelSerializer):

	class Meta:
		model = RecibosItems
		fields = "__all__"


class RecibosAlmacenSerializer(serializers.ModelSerializer):
	
	items = RecibosItemsSerializer(many=True, source="recibo_items")

	class Meta:
		model = RecibosAlmacen
		fields = "__all__"

class TicketsSerializer(serializers.ModelSerializer):

	class Meta:
		model = Tickets
		fields = "__all__"

class CargaSerializer(serializers.ModelSerializer):

	class Meta:
		model = Carga
		fields = "__all__"	

class ChoferSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ["id", "username", "first_name", "last_name", "is_staff", "is_active", "planta_id", "getRolAlias"]

class MovimientoSerializer(serializers.ModelSerializer):

	planta = PlantaSerializer()
	chofer = ChoferSerializer()
	relevo = ChoferSerializer()
	cargas = CargaSerializer(many=True, source="carga_set")

	class Meta:
		model = Movimiento
		fields = "__all__"		

class TicketsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tickets
		fields = "__all__"		

class EvidenciaIncidenteVialSerializer(serializers.ModelSerializer):
	class Meta:
		model = EvidenciaIncidenteVial
		fields = "__all__"
		

class IncidenteVialSerializer(serializers.ModelSerializer):
	evidencia = EvidenciaIncidenteVialSerializer(many=True, source="evidencia_incidente_vial")

	class Meta:
		model = IncidenteVial
		fields = "__all__"	

class GuardTrackingSerializer(serializers.ModelSerializer):
	class Meta:
		model = GuardTracking
		fields = "__all__"	
		


			
		
			




