from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from API.serializers import RondinSerializer
from entorno.models import Incidente
from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_18_puntos_Trailer, F_Visitantes, EntradaEquipo, Incidentes
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.contrib import auth, messages
from core.models import Planta, Cliente, User, Role
from core import user_validation
from django.http import HttpResponseRedirect, JsonResponse
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.sites.models import Site  
from arnes.models import Papeleta, Respuesta, Recomendacion, Pregunta

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']

def admin_papeletas(request):    
	if(request.user.getRolU() == "administrador"):
		papeletas = Papeleta.objects.all().order_by('-fecha')
		papeletas = filterEncuestas(papeletas)
	else:
		plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
		papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
		papeletas = filterEncuestas(papeletas)

	return render(request, 'administrador/arnes/papeletas.html', { 'css_list': css_list, 'js_list': js_list, 'papeletas': papeletas })

def admin_papeleta_detalle(request, id):
    papeleta = Papeleta.objects.get(pk=id)
    return render(request, 'administrador/arnes/papeleta_detalle.html', { 'css_list': css_list, 'js_list': js_list, 'papeleta': papeleta })

def admin_papeleta_recomendacion_crear(request, id, respuesta_id):
	papeleta = Papeleta.objects.get(pk=id)
	respuesta = Respuesta.objects.get(pk=respuesta_id)

	if request.method == "POST":
		recomendacion = Recomendacion()
		#recomendacion.nombre = request.nombre
		recomendacion.descripcion = request.POST.get('descripcion')
		recomendacion.ponderacion = request.POST.get('ponderacion')
		#recomendacion.vulnerabilidad = request.vulnerabilidad
		recomendacion.costo = request.POST.get('costo')
		try:
			recomendacion.evidencia = request.FILES['evidencia']
		except:
			print("no file")
		recomendacion.fecha_compromiso = request.POST.get('fecha_compromiso')
		recomendacion.user_aguilas = request.user
		recomendacion.papeleta_id = id
		recomendacion.respuesta_id = respuesta_id

		recomendacion.save();
		return redirect("administrador:admin_papeleta_detalle", id=id)

	return render(request, 'administrador/arnes/recomendacion_form.html', { 'css_list': css_list, 'js_list': js_list, 'papeleta': papeleta, 'respuesta': respuesta })

def admin_papeleta_recomendacion_edit(request, id):
	recomendacion = Recomendacion.objects.get(pk=id)

	if request.method == "POST":
		recomendacion.status = request.POST.get('status')
		recomendacion.descripcion = request.POST.get('descripcion')
		recomendacion.ponderacion = request.POST.get('ponderacion')
		#recomendacion.vulnerabilidad = request.vulnerabilidad
		recomendacion.costo = request.POST.get('costo')
		try:
			recomendacion.evidencia = request.FILES['evidencia']
		except:
			print("no file")
		recomendacion.fecha_compromiso = request.POST.get('fecha_compromiso')
		recomendacion.user_aguilas = request.user

		recomendacion.save();
		return redirect('administrador:admin_papeleta_detalle', id=recomendacion.papeleta_id)

	return render(request, 'administrador/arnes/recomendacion_update_form.html', { 'css_list': css_list, 'js_list': js_list, 'recomendacion': recomendacion })


def filterEncuestas(papeletas):
	#get distings plantas
	plantas_ids = []
	for p in papeletas:
		if p.planta_id not in plantas_ids:
			plantas_ids.append(p.planta_id)
			print("agregada Planta "+str(p.planta_id))


	pencuestas = []
	pencuestas_ids = []
	p_ids = []
	#for each planta
	for pid in plantas_ids:
		print("evaluando Planta "+str(pid))
		pfiltered = papeletas.filter(planta_id=pid)
		#each papelete in planta
		
		pencuestas_ids = []
		#tomar encuesta mas reciente de cada una diferente
		for penc in pfiltered.order_by("encuesta_id", "-fecha"):
			print("evaluando "+str(penc.encuesta_id))
			if penc.encuesta_id not in pencuestas_ids:
				pencuestas.append(penc)
				print("papeleta "+str(penc.id))
				p_ids.append(penc.id)
				pencuestas_ids.append(penc.encuesta_id)
				print("agregada "+str(penc))
			
	print("pids "+str(p_ids))
	print("enc_ids "+str(pencuestas_ids))
	print("papeletas "+str(pencuestas))
	#papeletas filtradas por la mas recientes de cada tipo
	papeletas = papeletas.filter(id__in=p_ids).all()

	return papeletas

def admin_papeleta_nueva_evidencia(request, id, id_pregunta):
	
	papeleta = Papeleta.objects.get(pk=id)
	pregunta = Pregunta.objects.get(pk=id_pregunta)
	respuesta = Respuesta.objects.filter(papeleta_id=id, pregunta_id=id_pregunta).first()

	if request.method == 'POST':

		myfile =request.FILES['evidenciafile']
   
		fs = FileSystemStorage(location="/var/www/vhosts/panoptic.com.mx/httpdocs/mxpanoptic/media/evidencia/papeletas/"+str(id)+"/"+str(id_pregunta))
		#fs = FileSystemStorage(location="/media/evidencia/papeletas/"+str(id)+"/"+str(id_pregunta))
		filename = fs.save(myfile.name, myfile)
		print(filename)

		return redirect('administrador:admin_papeleta_detalle', id=id)

	return render(request, 'administrador/arnes/papeleta_evidencia_form.html', { 'css_list': css_list, 'js_list': js_list, 'papeleta': pregunta, "pregunta": pregunta, "respuesta": respuesta })
