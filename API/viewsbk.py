from django.shortcuts import render, HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes, authentication_classes, permission_classes
from .serializers import *
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from analytics.models import Rondin, RondinHecho, PuntoHecho, EvidenciaPunto, EvidenciaPunto, F_Visitantes, F_ES_Trailers, F_18_puntos_Trailer, Incidentes, EntradaEquipo, ItemEntradaEquipo,  GuardTracking, EntradaMateriales, ItemEntradaMaterial, EntradaVehiculo, Paqueteria, Empleado_Sin_Gafete, Area_Restringida, RecibosItems, RecibosAlmacen, GuardTracking
from arnes.models import Encuesta, Papeleta, Respuesta
from core.models import Cliente, Notificacion, Planta
from core.utils import *
from ddmanagement.models import *
from cporte.models import *
import datetime
from django.contrib.auth import authenticate
from django.core.files.storage import FileSystemStorage
from rest_framework.renderers import JSONRenderer
from shapely.geometry import Point, Polygon
import json
from core import notifications
import requests
import facturama
from django.http import (HttpResponseBadRequest)

class rondinList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        rondines = Rondin.objects.all()
        serializer = RondinSerializer(rondines, many=True)
        return Response(serializer.data)


class RondinStart(APIView):

    def get(self, request, *args, **kwargs):
        print(request.data)

        rondin = Rondin.objects.get(pk=1)
        rondinhecho = RondinHecho()
        rondinhecho.rondin = rondin
        # rondinhecho.save()

        serializer = RondinHechoSerializer()

        return Response(serializer.data)

class TrasladoId(APIView):

    def get(self, request, *args, **kwargs):
        parms = { 
            'id':request.GET.get('id'),
        }
        traslado = PorteCarta.objects.get(id=parms["id"])
        serializer = TrasladoSerializer(traslado, many=False)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        traslado = PorteCarta.objects.get(id = request.GET.get('id'))
        traslado.json = json.loads(request.POST.get('json'))
        try:
            res = facturama.CfdiMultiEmisor.create(traslado.json)
            traslado.pdf = facturama.CfdiMultiEmisor.get_by_file("pdf","issuedLite",res["Id"])["Content"]
            traslado.status = 1
        except Exception as e:
            return Response({"Message": e})
        traslado.save()
        return Response({"Message": "REGISTRADO COMPLEADO"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_load_rondin(request):

    rondin = Rondin.objects.get(pk=request.POST.get("rondin_id"))

    serializer = RondinSerializer(rondin)

    return Response(serializer.data)


@api_view(["POST"])
def api_start_rondin(request):

    rondin = Rondin.objects.get(pk=request.POST.get("rondin_id"))
    rondinhecho = RondinHecho()
    rondinhecho.hora_inicio = datetime.datetime.now()
    rondinhecho.rondin = rondin
    rondinhecho.save()

    serializer = RondinHechoSerializer(rondinhecho)

    return Response(serializer.data)

class AnalyticsViews(APIView):
    def get(self, request):
        if "id" not in request.GET:
            return HttpResponseBadRequest()
        else:
            planta_id = request.GET["id"]
            cantRondines, incidenciasRondines = getRondines(planta_id)
            cobertura = getCobertura(planta_id)
            cant18puntos, incidencias18puntos = get18puntos(planta_id)   
            vgeneral = getVulnerabilidadGeneral(planta_id)
            #getVulnerabilidadGeneral(planta_id)
 
            json = {
                "rondines": cantRondines,
                "incidenciasRondines": incidenciasRondines,
                "cobertura": cobertura,
                "18puntos": cant18puntos,
                "incidencias18puntos": incidencias18puntos,
                "vulnerabilidadGeneral": vgeneral,
                "seguridad": 100 - vgeneral
            }
            return Response(json)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_markers_list(request):
    print(request.user.cliente_id) 
    cliente = Cliente.objects.get(pk=request.user.cliente_id)

    serializer = ClienteSerializer(cliente)
    
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_get_patio(request):
    
    planta = request.user.planta_id

    try:
        patio = Patio.objects.get(planta_id=planta)
    except Patio.DoesNotExist:
        patio = None
    
    serializer = PatioSerializer(patio)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_store_rondin_hecho(request):
    
    rondin = Rondin.objects.get(pk=request.POST.get("rondin_id"))
    rondinhecho = RondinHecho()
    rondinhecho.hora_inicio = request.POST.get("hora_inicio")
    rondinhecho.hora_fin = request.POST.get("hora_fin")
    rondinhecho.guardia_id = request.POST.get("guardia_id")
    rondinhecho.rondin = rondin
    rondinhecho.save()
    
    puntohecho_punto = request.POST.getlist("puntohecho_punto[]")
    puntohecho_inicio = request.POST.getlist("puntohecho_inicio[]")
    puntohecho_fin = request.POST.getlist("puntohecho_fin[]")
    puntohecho_nota = request.POST.getlist("puntohecho_nota[]")
    puntohecho_evidenciaid = request.POST.getlist("puntohecho_evidenciaid[]")

    notificationCheck = False

    for i in range(len(puntohecho_punto)):
        puntohecho = PuntoHecho()
        puntohecho.punto_id = puntohecho_punto[i]
        puntohecho.rondinhecho = rondinhecho
        puntohecho.hora_inicio = puntohecho_inicio[i]
        puntohecho.hora_fin = puntohecho_fin[i]
        puntohecho.save()
       
        evidenciaPhotoExist = bool(request.FILES.get("puntohecho_evidencia"+puntohecho_punto[i],False))

        if puntohecho_nota[i] != "" or evidenciaPhotoExist:
            evidencia = EvidenciaPunto()
            evidencia.punto_id = puntohecho_punto[i]
            evidencia.rondinhecho = rondinhecho
            evidencia.nota = puntohecho_nota[i]

            if evidenciaPhotoExist:
                evidencia.evidencia = request.FILES["puntohecho_evidencia"+puntohecho_punto[i]]
                
            notificationCheck = True
            evidencia.save() 

        """
        for j in range(len(puntohecho_evidenciaid)):
            if puntohecho_punto[i] == puntohecho_evidenciaid[j]:
                evidencia = EvidenciaPunto()
                evidencia.punto_id = puntohecho_punto[i]
                evidencia.rondinhecho = rondinhecho
                evidencia.nota = puntohecho_nota[i]
                if bool(request.FILES.get("puntohecho_evidencia"+puntohecho_punto[i], False)) == True:
                    evidencia.evidencia = request.FILES["puntohecho_evidencia" +
                                                        puntohecho_punto[i]]

                evidencia.save()
        """
    serializer = RondinHechoSerializer(rondinhecho)
    
    if notificationCheck:
        noti = Notificacion()
        noti.titulo = "Rondin con evidencias"
        noti.mensaje = "Se realizó un rondin '" + \
            str(rondinhecho.rondin.nombre)+"' con evidencias en la planta " + \
            str(rondinhecho.rondin.planta.nombre)
        noti.modelo = "RondinHecho"
        noti.idproblema = rondinhecho.id
        noti.param_bol = False
        noti.usuario_id = request.user.id
        noti.save()

        try:
            print("mandar notificacion")
            notifications.sendNotification("Rondin con evidencia", "Se realizó un rondin '"+str(
                rondinhecho.rondin.nombre)+"' con evidencias en la planta "+str(rondinhecho.rondin.planta.nombre), request.user.notification_token, request.user.email, noti)
        except:
            print("No se pudo enviar notificacion")

        try:
            print("mandar notificación por planta")
            notifications.sendemailsbyplanta("Rondin con evidencia", "Se realizó un rondin '"+str(
                rondinhecho.rondin.nombre)+"' con evidencias en la planta "+str(rondinhecho.rondin.planta.nombre), rondinhecho.rondin.planta, "predictive", noti)
        except Exception as error2:
            print("No se pudo enviar notificación por plantas: "+str(error2))
    
    return Response(serializer.data)

@api_view(["POST"])
def api_add_punto_hecho(request):

    def initialize_request(self, request, *args, **kwargs):
        if not isinstance(request, Request):
            request = super().initialize_request(request, *args, **kwargs)
        return request

    punto = PuntoHecho()
    punto.punto_id = request.POST.get("punto_id")
    punto.rondinhecho_id = request.POST.get("rondinhecho_id")
    punto.save()

    serializer = PuntoHechoSerializer(punto)

    return Response(serializer.data)


@api_view(["POST"])
def api_finalizar_rondin(request):

    rondinhecho = RondinHecho.objects.get(
        pk=request.POST.get("rondinhecho_id"))
    now = datetime.datetime.now()
    rondinhecho.hora_fin = now
    rondinhecho.save()

    serializer = RondinHechoSerializer(rondinhecho)

    return Response(serializer.data)


@api_view(["POST"])
def api_agregar_evidencia(request):
    name = request.FILES['evidencia'].name
    evidencia = EvidenciaPunto()
    evidencia.nota = request.POST.get("nota")

    serializer = EvidenciaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def api_login(request):
    user = authenticate(username=request.POST.get(
        'username'), password=request.POST.get('password'))

    if user is None:
        return HttpResponse("{'error': 'Credenciales incorrectas'}")

    # return HttpResponse(user)
    #token = Token.objects.get_or_create(user=user)

    user.enservicio = True
    user.save()

    serializer = LoginUserSerializer(user)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_logout(request):
    user = request.user

    if user is None:
        return HttpResponse("{'error': 'No se puede autencicar al usuario'}")
    # return HttpResponse(user)
    #token = Token.objects.get_or_create(user=user).first()

    user.enservicio = False
    user.save()

    return HttpResponse("{'success': 'OK'}")


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fvisitantes(request):
    if request.POST.get("pre") == "1":
        previsitante = F_Visitantes.objects.get(pk=request.POST.get("id"))
        if previsitante.pre == 0:
            return Response({'response': '401'}, status.HTTP_400_BAD_REQUEST)
        previsitante.pre = 0
        previsitante.gafete = request.POST.get("gafete")
        previsitante.entrada = request.POST.get("entrada")
        previsitante.ine_frontal = request.FILES["ine_frontal"]
        previsitante.ine_posterior = request.FILES["ine_posterior"]

        try:
            previsitante.save()
            json = {'response': '201'}
            return Response(json,status = status.HTTP_201_CREATED)
        except Exception as e:
            json = {'response': '400'}
            return Response(json,status = status.HTTP_400_BAD_REQUEST)
    else:
        serializer = FVisitantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fvisitantes_list(request):

    fvisitantes = F_Visitantes.objects.filter(
        planta_id=request.POST.get("planta_id")).filter(pre=0)
    #fvisitantes = F_Visitantes.objects.all();

    serializer = FVisitantesSerializer(fvisitantes, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fvisitantes_salida(request):

    #fvisitantes = F_Visitantes.objects.filter(planta_id=request.POST.get("planta_id"))
    fvisitante = F_Visitantes.objects.get(pk=request.POST.get("fvisitante_id"))
    fvisitante.salida = request.POST.get("salida")
    fvisitante.save()

    serializer = FVisitantesSerializer(fvisitante)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fes_trilers(request):

    c = request.POST.get("cajon_id")
    serializer = FESTrailersSerializer(data=request.data)
    
    if serializer.is_valid():
        idaux = serializer.save()
        if c is not None:
            cajon = Cajon.objects.get(pk=c)
            cajon.disponibilidad = 0
            cajon.tipo_caja = request.POST.get("tipo_caja") 
            cajon.trailer_id = idaux.id
            cajon.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fes_trilers_list(request):

    #fvisitantes = F_Visitantes.objects.filter(planta_id=request.POST.get("planta_id"))
    #festrailers = F_ES_Trailers.objects.all()
    festrailers = F_ES_Trailers.objects.filter(planta_id=request.POST.get("planta_id"))

    serializer = FESTrailersSerializer(festrailers, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_fes_trilers_salida(request):

    festrailers = F_ES_Trailers.objects.get(
        pk=request.POST.get("festrailers_id"))
    festrailers.salida = request.POST.get("salida")
    festrailers.save()
    
    cajon = Cajon.objects.filter(trailer_id=festrailers.id).first()
    
    if cajon is not None:
        cajon.trailer_id = None
        cajon.tipo_caja = None
        cajon.disponibilidad = 2
        cajon.save()

    serializer = FESTrailersSerializer(festrailers)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_revision_18_puntos(request):

    serializer = F18puntosTrailerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_reportar_incidente(request):

    serializer = IncidentesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        planta = Planta.objects.get(id=request.POST.get('planta'))
        noti = Notificacion()
        noti.titulo = "Incidente de servicio"
        noti.mensaje = "Se dio de alta un incidente de servicio"
        noti.modelo = "Incidentes"
        noti.idproblema = serializer.data['id']
        noti.usuario_id = request.user.id
        noti.save()

        try:
            print("mandar notificación")
            notifications.sendNotification("Incidente de servicio", "Se dio de alta un incidente de servicio en unidad de negocio: " +
                                           planta.nombre, request.user.notification_token, request.user.email, noti)
        except Exception as error1:
            print("No se pudo enviar notificación: "+str(error1))

        try:
            print("mandar notificación por planta")
            notifications.sendemailsbyplanta("Incidente de servicio", "Se dio de alta un incidente de servicio en unidad de negocio: " +
                                             planta.nombre+"\nReportado por: "+str(request.user)+"\nNota: "+request.POST.get('nota'), planta, "predictive", noti)
        except Exception as error2:
            print("No se pudo enviar notificación: "+str(error2))

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def api_entrada_equipo(request):

    entrada = EntradaEquipo()
    if 'visitante_id' in request.POST:
        entrada.visitante_id = request.POST.get("visitante_id")
    entrada.planta_id = request.POST.get("planta")
    entrada.fecha = request.POST.get("fecha")
    entrada.guardia_id = request.POST.get("guardia")
    entrada.nombre = request.POST.get("nombre")
    entrada.save()

    descripciones = request.POST.getlist("descripcion[]")
    series = request.POST.getlist("n_serie[]")
    cantidades = request.POST.getlist("cantidad[]")

    for i in range(len(descripciones)):
        item = ItemEntradaEquipo()
        item.entradaequipo = entrada
        item.descripcion = descripciones[i]
        item.n_serie = series[i]
        item.cantidad = cantidades[i]
        item.save()

    serializer = EntradaEquipoSerializer(entrada)
    return Response(serializer.data)


@api_view(["POST"])
def api_entrada_equipo_get(request):
    entrada = EntradaEquipo.objects.filter(
        visitante_id=request.POST.get("visitante_id")).first()

    serializer = EntradaEquipoSerializer(entrada)
    return Response(serializer.data)


@api_view(["POST"])
def api_entrada_material_get(request):

    entrada = EntradaMateriales.objects.filter(
        visitante_id=request.POST.get("visitante_id")).first()

    serializer = EntradaMaterialesSerializer(entrada)
    return Response(serializer.data)


@api_view(["POST"])
def api_entrada_materiales(request):
    entrada = EntradaMateriales()
    if 'visitante' in request.POST:
        entrada.visitante_id = request.POST.get("visitante")
    entrada.planta_id = request.POST.get("planta")
    entrada.fecha = request.POST.get("fecha")
    entrada.guardia_id = request.POST.get("guardia")
    entrada.nombre = request.POST.get("nombre")
    entrada.save()

    descripciones = request.POST.getlist("descripcion[]")
    tipos = request.POST.getlist("tipo[]")

    for i in range(len(descripciones)):
        item = ItemEntradaMaterial()
        item.entradamateriales = entrada
        item.descripcion = descripciones[i]
        item.tipo = tipos[i]
        item.save()

    serializer = EntradaMaterialesSerializer(entrada)
    return Response(serializer.data)


@api_view(["POST"])
def api_entrada_vehiculo(request):
    entrada = EntradaVehiculo()
    entrada.visitante_id = request.POST.get("visitante")
    entrada.planta_id = request.POST.get("planta")
    entrada.fecha = request.POST.get("fecha")
    entrada.guardia_id = request.POST.get("guardia")
    entrada.marca = request.POST.get("marca")
    entrada.modelo = request.POST.get("modelo")
    entrada.placas = request.POST.get("placas")
    entrada.nota = request.POST.get("nota")
    entrada.save()

    serializer = EntradaVehiculoSerializer(entrada)
    return Response(serializer.data)


@api_view(["POST"])
def api_entrada_vehiculo_get(request):
    vehiculo = EntradaVehiculo.objects.filter(
        visitante_id=request.POST.get("visitante_id")).first()

    serializer = EntradaVehiculoSerializer(vehiculo)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_registro_paqueteria(request):
    paqueteria = Paqueteria()
    paqueteria.guia = request.POST.get("guia")
    paqueteria.nombre = request.POST.get("nombre")
    paqueteria.empresa = request.POST.get("empresa")
    paqueteria.fecha = request.POST.get("fecha")
    paqueteria.bolfaltainfo = request.POST.get("bolfaltainfo")
    paqueteria.bolcables = request.POST.get("bolcables")
    paqueteria.bolpolvo = request.POST.get("bolpolvo")
    paqueteria.bololor = request.POST.get("bololor")
    paqueteria.bolfuerahorario = request.POST.get("bolfuerahorario")
    paqueteria.nota = request.POST.get("nota")
    paqueteria.destinatario = request.POST.get("destinatario")
    paqueteria.user_aguilas_id = request.POST.get("guardia")
    paqueteria.un_id = request.POST.get("planta")
    paqueteria.save()

    serializer = PaqueteriaSerializer(paqueteria)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_empleado_singafete(request):
    empleado = Empleado_Sin_Gafete()
    empleado.planta_id = request.POST.get("planta")
    empleado.user_aguilas_id = request.POST.get("user_aguilas")
    empleado.no_emp = request.POST.get("no_emp")
    empleado.empleado = request.POST.get("empleado")
    empleado.departamento = request.POST.get("departamento")
    empleado.bolgafetepersonal = request.POST.get("bolgafetepersonal")
    empleado.bolgafetevehicular = request.POST.get("bolgafetevehicular")
    empleado.jefe = request.POST.get("jefe")
    empleado.turno = request.POST.get("turno")
    empleado.fecha = request.POST.get("fecha")
    empleado.motivo = request.POST.get("motivo")

    empleado.save()

    serializer = EmpleadiGafeteSerializer(empleado)
    return Response(serializer.data)


@api_view(["POST"])
def api_empleado_singafete_list(request):
    empleados = Empleado_Sin_Gafete.objects.filter(
        planta_id=request.POST.get("planta_id"), fecha_salida__isnull=True)

    serializer = EmpleadiGafeteSerializer(empleados, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_empleado_singafete_salida(request):
    empleado = Empleado_Sin_Gafete.objects.filter(
        id=request.POST.get("id")).first()
    empleado.fecha_salida = request.POST.get("salida")

    empleado.save()

    serializer = EmpleadiGafeteSerializer(empleado)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_acceso_area_restringida(request):
    acceso = Area_Restringida()

    acceso.no_emp = request.POST.get("no_emp")
    acceso.nombre = request.POST.get("nombre")
    acceso.departamento = request.POST.get("departamento")
    acceso.fecha = request.POST.get("fecha")
    acceso.anfitrion = request.POST.get("anfitrion")
    acceso.tiempo = request.POST.get("tiempo")
    acceso.nota = request.POST.get("nota")
    acceso.planta_id = request.POST.get("planta")
    acceso.user_aguilas_id = request.POST.get("guardia")

    acceso.save()

    serializer = AreaRestringidaSerializer(acceso)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_acceso_area_restringida_salida(request):
    acceso = Area_Restringida.objects.filter(id=request.POST.get("id")).first()
    acceso.fecha_salida = request.POST.get("salida")

    acceso.save()

    serializer = AreaRestringidaSerializer(acceso)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_acceso_area_restringida_list(request):
    accesos = Area_Restringida.objects.filter(
        planta_id=request.POST.get("planta_id"), fecha_salida__isnull=True)

    serializer = AreaRestringidaSerializer(accesos, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_recibos_almacen(request):
    recibo = RecibosAlmacen()

    recibo.no_emp = request.POST.get("no_emp")
    recibo.empleado = request.POST.get("nombre")
    recibo.fecha = request.POST.get("fecha")
    recibo.departamento = request.POST.get("departamento")
    recibo.jefe = request.POST.get("jefe")
    recibo.turno = request.POST.get("turno")
    recibo.planta_id = request.POST.get("planta")
    recibo.user_aguilas_id = request.POST.get("guardia")

    recibo.proveedor = request.POST.get("proveedor")
    recibo.empresa = request.POST.get("empresa")
    recibo.num_economico = request.POST.get("num_economico")
    recibo.num_caja = request.POST.get("num_caja")

    recibo.save()

    cantidades = request.POST.getlist("cantidad[]")
    unidades = request.POST.getlist("unidad[]")
    descripciones = request.POST.getlist("desc[]")
    nopartes = request.POST.getlist("noparte[]")
    origenes = request.POST.getlist("origen[]")
    destinos = request.POST.getlist("destino[]")

    for i in range(len(cantidades)):
        item = RecibosItems()
        item.recibo_id = recibo.id
        item.cantidad = cantidades[i]
        item.unidad = unidades[i]
        item.desc = descripciones[i]
        item.noparte = nopartes[i]
        item.origen = origenes[i]
        item.destino = destinos[i]
        item.fecha = request.POST.get("fecha")
        item.save()

    serializer = RecibosAlmacenSerializer(recibo)
    return Response(serializer.data)

 # ===============================ERNES============================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_load_encuestas(request):

    encuestas = Encuesta.objects.all()

    serializer = EncuestaSerializer(encuestas, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_new_encuesta_papeleta(request):
    
    papeleta = Papeleta()
    papeleta.planta_id = request.POST.get("planta_id")
    papeleta.encuesta_id = request.POST.get("encuesta_id")
    papeleta.user_aguilas_id = request.POST.get("user_id")
    papeleta.fecha = request.POST.get("fecha")

    respuestas = request.POST.getlist('respuesta[]')
    valores = request.POST.getlist('valor[]')
    requeridos = request.POST.getlist('requerido[]')
    cumplidos = request.POST.getlist('cumple[]')
    ocurrencias = request.POST.getlist('ocurrencia[]')
    impactos = request.POST.getlist('impacto[]')
    observaciones = request.POST.getlist('observaciones[]')
    preguntas = request.POST.getlist('pregunta[]')
    preguntas_id = request.POST.getlist('pregunta_id[]')
    evidenciasPreguntaID = request.POST.getlist('evidenciapreguntaid[]')
    papeleta.save()

    for i in range(len(respuestas)):
        # return HttpResponse(preguntas[i])
        respuesta = Respuesta()
        respuesta.papeleta_id = papeleta.id
        respuesta.pregunta_text = preguntas[i]
        respuesta.pregunta_id = preguntas_id[i]
        respuesta.valor = valores[i]
        respuesta.respuesta = respuestas[i]
        respuesta.requiere_evidencia = requeridos[i]
        respuesta.cumple = cumplidos[i]
        respuesta.ocurrencia = ocurrencias[i]
        respuesta.impacto = impactos[i]
        respuesta.observacion = observaciones[i]
        respuesta.resultado = int(respuesta.ocurrencia)*int(respuesta.impacto)
        respuesta.save()

    for i in range(len(evidenciasPreguntaID)):
        myfile = request.FILES['evidenciafile'+str(i)]
        fs = FileSystemStorage(location="/var/www/vhosts/panoptic.com.mx/httpdocs/mxpanoptic/media/evidencia/papeletas/"+str(papeleta.id)+"/"+evidenciasPreguntaID[i]) 
        #fs = FileSystemStorage(location="/home/ubuntu/pgit/media/evidencia/papeletas/" +
        #                       str(papeleta.id)+"/"+evidenciasPreguntaID[i])
        filename = fs.save(myfile.name, myfile)
        print(filename)

    serializer = PapeletaSerializer(papeleta)

    noti = Notificacion()
    noti.titulo = "Análisis de riesgo hecho"
    noti.mensaje = "Se dio de alta un análisis de riesgo de "+str(papeleta.encuesta.nombre)+" para cliente "+str(
        request.user.cliente.nombre)+" en planta "+str(request.user.planta.nombre)
    noti.modelo = "Papeleta"
    noti.idproblema = papeleta.id
    noti.param_bol = False
    noti.usuario_id = request.user.id
    noti.save()

    try:
        print("mandar notificacion")
        notifications.sendNotification("Análisis de riesgo hecho", "Se dio de alta un análisis de riesgo de "+str(papeleta.encuesta.nombre)+" para cliente "+str(
            request.user.cliente.nombre)+" en planta "+str(request.user.planta.nombre), request.user.notification_token, request.user.email, noti)
    except:
        print("No se pudo enviar notificacion")

    try:
        print("mandar notificación por planta")
        notifications.sendemailsbyplanta("Análisis de riesgo hecho", "Se dio de alta un análisis de riesgo de "+str(papeleta.encuesta.nombre) +
                                         " para cliente "+str(request.user.cliente.nombre)+" en planta "+str(request.user.planta.nombre), papeleta.planta, "arnes", noti)
    except Exception as error2:
        print("No se pudo enviar notificación: "+str(error2))

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_list_clientes(request):

    clientes = Cliente.objects.all()

    serializer = ClienteSerializer(clientes, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def api_update_tracking(request):
    tracking = GuardTracking()

    tracking.planta_id = request.POST.get("planta")
    tracking.user_id = request.POST.get("user")
    tracking.lat = request.POST.get("lat")
    tracking.lng = request.POST.get("lng")
    tracking.save()

    # checar punto dentro de area
    pt = Point(float(request.POST.get("lat")), float(request.POST.get("lng")))
    polygon = tracking.planta.polyradio
    if polygon != None:
        js = json.loads(polygon)
        print(js[0])
        poly = Polygon(js[0])
        if poly.contains(pt) != True:
            try:
                print("mandar notificacion de gpstracking")
                notifications.sendNotification(
                    "Geocerca", "Esta fuera de zona de planta ", tracking.user.notification_token, "")
            except:
                print("No se pudo enviar notificacion")

    return HttpResponse("{'success': 'coordenadas guardadas'}")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def api_list_movimientos(request):
    movimientos = Movimiento.objects.filter(confirmacion=False).all()

    serializer = MovimientoSerializer(movimientos, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_confirmar_llegada_movimiento(request):
    movimiento = Movimiento.objects.filter(
        id=request.POST.get("movimiento_id")).first()
    movimiento.confirmacion = True
    movimiento.fecha_fin = request.POST.get("fecha_fin")

    movimiento.save()
    serializer = MovimientoSerializer(movimiento)

    return Response(serializer.data)


@api_view(["POST"])
def api_agregar_ticket(request):
    ticket = Tickets()
    ticket.movimiento_id = request.POST.get("movimiento_id")
    ticket.imagen = request.FILES['imagen']

    ticket.save()
    serializer = TicketsSerializer(ticket)

    return Response(serializer.data)


@api_view(["POST"])
def api_registrar_incidente_vial(request):
    incidente = IncidenteVial()
    incidente.movimiento_id = request.POST.get("movimiento_id")
    incidente.tipo = request.POST.get("tipo")
    incidente.notas = request.POST.get("notas")
    incidente.fecha = request.POST.get("fecha")
    incidente.ubigpslat = request.POST.get("ubigpslat")
    incidente.ubigpslng = request.POST.get("ubigpslng")
    incidente.save()

    for i in range(int(request.POST.get("filesize"))):
        evidencia = EvidenciaIncidenteVial()
        evidencia.incidente = incidente
        evidencia.evidencia = request.FILES['files'+str(i)]
        evidencia.save()

    serializer = IncidenteVialSerializer(incidente)

    movimiento = Movimiento.objects.get(id=request.POST.get("movimiento_id"))
    planta = movimiento.planta
    noti = Notificacion()
    noti.titulo = "Incidente de Movimiento"
    noti.mensaje = "Se dio de alta un incidente de movimiento"
    noti.modelo = "Movimiento"
    noti.idproblema = request.POST.get("movimiento_id")
    noti.param_bol = False
    noti.usuario_id = request.user.id
    noti.save()

    try:
        print("mandar notificacion")
        notifications.sendNotification("Incidente de movimiento", "Se dio de alta un incidente de movimiento para unidad de negocio: "+planta.nombre+"\nmovimiento origen: "+str(
            movimiento.origen)+"\nmovimiento destino: "+str(movimiento.destino), request.user.notification_token, request.user.email, noti)
    except:
        print("No se pudo enviar notificacion")

    try:
        print("mandar notificación por planta")
        notifications.sendemailsbyplanta("Incidente de movimiento", "Se dio de alta un incidente de movimiento para unidad de negocio: "+planta.nombre +
                                         "\nmovimiento origen: "+str(movimiento.origen)+"\nmovimiento destino: "+str(movimiento.destino), planta, "ddmanagement", noti)
    except Exception as error2:
        print("No se pudo enviar notificación: "+str(error2))

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_gpstracking_get(request):

    if(request.POST.get("modo") == "rango"):
        guardTracking = GuardTracking.objects.filter(user_id=request.POST.get(
            "user_id"), fecha__range=[request.POST.get("desde"), request.POST.get("hasta")]).all()
        serializer = GuardTrackingSerializer(guardTracking, many=True)
        return Response(serializer.data)

    guardTracking = GuardTracking.objects.filter(
        user_id=request.POST.get("user_id")).all()
    serializer = GuardTrackingSerializer(guardTracking, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def api_register_notification_token(request):
    user = request.user
    user.notification_token = request.POST.get('notification_token')
    user.save()

    return HttpResponse("{'success': 'token_registrado'}")

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_traslados_list(request):
    s = request.GET.get('status')
    traslados = PorteCarta.objects.filter(status=s)
    serializer = TrasladoSerializer(traslados, many=True)

    return Response(serializer.data)


@api_view(["GET"])
#@permission_classes([IsAuthenticated])
def get_traslado(request):
    parms = {
        'id':request.GET.get('id'),
    }
    traslado = PorteCarta.objects.get(id=parms["id"])
    serializer = TrasladoSerializer(traslado, many=False)
    return Response(serializer.data)

@api_view(["GET"])
def get_gps_list(request):
    params = {
        'key': request.GET.get('key'),
        'unit_id': request.GET.get('unit_id'),
    }
    url = "https://gps.ubitech.mx/api/v1/unit/list.json?key=" + \
        request.GET.get('key')+"&unit_id="+request.GET.get('unit_id')

    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        return Response(response.json())
    else:
        return HttpResponse("error code: "+response.status_code)

@api_view(["POST"])
def gps_tracker(request):
    print(request.body)
    return Response()
