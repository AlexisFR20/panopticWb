from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404, HttpResponse
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
from arnes.models import Categoria_Encuesta, Papeleta
from django.db.models import Avg

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker',  'js_fancybox']

def admin_resultados_analisis_riesgo(request):
	if(request.user.getRolU() == "administrador"):
		clientes = Cliente.objects.all()
		plantas = Planta.objects.all()
		#papeletas = Papeleta.objects.all().order_by('fecha').reverse()
		#papeletas = filterEncuestas(papeletas)
	elif(request.user.getRolU() == "auditor"):
		papeletas = Papeleta.objects.filter(user_aguilas=request.user).all()
		papeletas = filterEncuestas(papeletas)
		plantas_ids = []
		clientes_ids = []
		for p in papeletas:
			if p.planta_id not in plantas_ids:
				plantas_ids.append(p.planta_id)
				print("agregada Planta "+str(p.planta_id))

			if p.planta.cliente_id not in clientes_ids:
				clientes_ids.append(p.planta.cliente_id)
				print("Agregado Cliente "+str(p.planta.cliente_id))

		plantas = Planta.objects.filter(id__in=plantas_ids).all()
		clientes = Cliente.objects.filter(id__in=clientes_ids)
	elif(request.user.getRolU() == "ceo"):
		clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
		plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
		
	else:
		clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
		plantas = Planta.objects.filter(id=request.user.planta_id).all()

		
	return render(request, 'administrador/analisis_riesgo/resultados_analisis_riesgo.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes })

def admin_analisis_de_riesgo_road_map(request):
	if(request.user.getRolU() == "administrador"):
		clientes = Cliente.objects.all()
		plantas = Planta.objects.all()
		papeletas = Papeleta.objects.all().order_by('fecha').reverse()
		papeletas = filterEncuestas(papeletas)
	elif(request.user.getRolU() == "auditor"):
		papeletas = Papeleta.objects.filter(user_aguilas=request.user).all()
		papeletas = filterEncuestas(papeletas)
		plantas_ids = []
		clientes_ids = []
		for p in papeletas:
			if p.planta_id not in plantas_ids:
				plantas_ids.append(p.planta_id)
				print("agregada Planta "+str(p.planta_id))

			if p.planta.cliente_id not in clientes_ids:
				clientes_ids.append(p.planta.cliente_id)
				print("Agregado Cliente "+str(p.planta.cliente_id))

		plantas = Planta.objects.filter(id__in=plantas_ids).all()
		clientes = Cliente.objects.filter(id__in=clientes_ids)
	elif(request.user.getRolU() == "ceo"):
		clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
		plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
		papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
		papeletas = filterEncuestas(papeletas)
	else:
		clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
		plantas = Planta.objects.filter(id=request.user.planta_id).all()
		papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
		papeletas = filterEncuestas(papeletas)
	
	return render(request, 'administrador/analisis_riesgo/analisis_de_riego_road_map.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'papeletas': papeletas })

def ajax_roadmap_tabla(request):
	if request.GET.get('planta_id') != "":
		papeletas = Papeleta.objects.filter(planta_id=request.GET.get('planta_id')).all().order_by('-fecha')
	else:
		papeletas = Papeleta.objects.filter(planta__cliente_id=request.GET.get('cliente_id')).all().order_by('-fecha')

	return render(request, 'administrador/analisis_riesgo/ajax_road_map_table_papeletas.html', {'css_list': css_list, 'js_list': js_list, 'papeletas': papeletas })

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

def admin_analisis_de_riesgo_revision(request): 
	if(request.user.getRolU() == "administrador"):
		clientes = Cliente.objects.all()
		plantas = Planta.objects.all()
		papeletas = Papeleta.objects.all().order_by('fecha').reverse()
		papeletas = filterEncuestas(papeletas)
	else:
		clientes = Cliente.objects.filter(id=request.user.cliente_id).all()
		plantas = Planta.objects.filter(cliente_id=request.user.cliente_id).all()
		papeletas = Papeleta.objects.filter(planta__in=plantas).all().order_by('-fecha')
		papeletas = filterEncuestas(papeletas)
    
	return render(request, 'administrador/analisis_riesgo/analisis_de_riego_revision.html', { 'css_list': css_list, 'js_list': js_list, 'plantas': plantas, 'clientes': clientes, 'papeletas': papeletas })

def ajax_vulnerabilidad_general(request):
	planta = request.GET.get("planta_id")
	cliente = request.GET.get("cliente_id")

	if planta and planta != "":
		papeletas = Papeleta.objects.filter(planta_id=planta).all().order_by('-fecha')
		infraestructura = papeletas.filter(encuesta__categoria_id=1).all() #id 1 para infraestructura
		vsegop = papeletas.filter(encuesta__categoria_id=2).all() #id 2 para Seguridad operativa
		vsegelec = papeletas.filter(encuesta__categoria_id=3).all() #id 3 para seguridad electronica
		vlogistica = papeletas.filter(encuesta__categoria_id=4).all() #id 4 para logistica
		ventorno = papeletas.filter(encuesta__categoria_id=5).all() #id 5 para entorno
	elif cliente:
		papeletas = Papeleta.objects.filter(planta__cliente_id=cliente).all().order_by('fecha').reverse()
		vinfraestructura = papeletas.filter(encuesta__categoria_id=1).all() #id 1 para infraestructura
		vsegop = papeletas.filter(encuesta__categoria_id=2).all() #id 2 para Seguridad operativa
		vsegelec = papeletas.filter(encuesta__categoria_id=3).all() #id 3 para seguridad electronica
		vlogistica = papeletas.filter(encuesta__categoria_id=4).all() #id 4 para logistica
		ventorno = papeletas.filter(encuesta__categoria_id=5).all() #id 5 para entorno

	else:
		papeletas = Papeleta.objects.filter(planta__cliente_id=request.user.cliente_id).all().order_by('fecha').reverse()
		vinfraestructura = papeletas.filter(encuesta__categoria_id=1).all() #id 1 para infraestructura
		vsegop = papeletas.filter(encuesta__categoria_id=2).all() #id 2 para Seguridad operativa
		vsegelec = papeletas.filter(encuesta__categoria_id=3).all() #id 3 para seguridad electronica
		vlogistica = papeletas.filter(encuesta__categoria_id=4).all() #id 4 para logistica
		ventorno = papeletas.filter(encuesta__categoria_id=5).all() #id 5 para entorno


	#get distings plantas
	plantas_ids = [] 
	for p in papeletas:
		if p.planta_id not in plantas_ids:
			plantas_ids.append(p.planta_id)
			#print("agregada Planta "+str(p.planta_id))


	pencuestas = []
	pencuestas_ids = []
	p_ids = []
	#for each planta
	for pid in plantas_ids:
		#print("evaluando Planta "+str(pid))
		pfiltered = papeletas.filter(planta_id=pid)
		#each papelete in planta
		
		pencuestas_ids = []
		#tomar encuesta mas reciente de cada una diferente
		for penc in pfiltered.order_by("encuesta_id", "-fecha"):
			#print("evaluando "+str(penc.encuesta_id))
			if penc.encuesta_id not in pencuestas_ids:
				pencuestas.append(penc)
				#print("papeleta "+str(penc.id))
				p_ids.append(penc.id)
				pencuestas_ids.append(penc.encuesta_id)
				#print("agregada "+str(penc))
			
	#print("pids "+str(p_ids))
	#print("enc_ids "+str(pencuestas_ids))
	#print("papeletas "+str(pencuestas))
	#papeletas filtradas por la mas recientes de cada tipo
	papeletas = Papeleta.objects.filter(id__in=p_ids)
	#agrupadas por categorias
	vinfraestructura = papeletas.filter(encuesta__categoria_id=1).all() #id 1 para infraestructura
	vsegop = papeletas.filter(encuesta__categoria_id=2).all() #id 2 para Seguridad operativa
	vsegelec = papeletas.filter(encuesta__categoria_id=3).all() #id 3 para seguridad electronica
	vlogistica = papeletas.filter(encuesta__categoria_id=4).all() #id 4 para logistica
	ventorno = papeletas.filter(encuesta__categoria_id=5).all() #id 5 para entorno


	#calculos de vulneravilidad promedio
	avgvinfra = 0
	avgvsegop = 0
	avgvsegelec = 0
	avgvlogi = 0
	avgvent = 0

	avgrinfra = 0
	avgrsegop = 0
	avgrsegelec = 0
	avgrlogi = 0
	avgrent = 0

	catInfraestructura = []
	catSegop = []
	catSegelc = []
	catLogistica = []
	catEntorno = []

	encuestas_ids = []
	encuestas_names = []
	

	for v in vinfraestructura:
		avgvinfra += v.calcularVulnerabilidad()/vinfraestructura.count()
		avgrinfra += v.calcularRiesgo()/vinfraestructura.count()
		if v.encuesta.nombre not in encuestas_names:
			encuestas_names.append(v.encuesta.nombre)
		jsonInfra = {"id": v.id, "nombre": v.encuesta.nombre, "vul": v.calcularVulnerabilidad(), "riesgo": v.calcularRiesgo() }
		catInfraestructura.append(jsonInfra)

	for v in vsegop:
		avgvsegop += v.calcularVulnerabilidad()/vsegop.count()
		avgrsegop += v.calcularRiesgo()/vsegop.count()
		if v.encuesta.nombre not in encuestas_names:
			encuestas_names.append(v.encuesta.nombre)
		jsonSegop = {"id": v.id, "nombre": v.encuesta.nombre, "vul": v.calcularVulnerabilidad(), "riesgo": v.calcularRiesgo()}
		catSegop.append(jsonSegop)

	for v in vsegelec:
		avgvsegelec += v.calcularVulnerabilidad()/vsegelec.count()
		avgrsegelec += v.calcularRiesgo()/vsegelec.count()
		if v.encuesta.nombre not in encuestas_names:
			encuestas_names.append(v.encuesta.nombre)
		jsonSegelc = {"id": v.id, "nombre": v.encuesta.nombre, "vul": v.calcularVulnerabilidad(), "riesgo": v.calcularRiesgo()}
		catSegelc.append(jsonSegelc)

	for v in vlogistica:
		avgvlogi += v.calcularVulnerabilidad()/vlogistica.count()
		avgrlogi += v.calcularRiesgo()/vlogistica.count()
		if v.encuesta.nombre not in encuestas_names:
			encuestas_names.append(v.encuesta.nombre)
		jsonLogistica = {"id": v.id, "nombre": v.encuesta.nombre, "vul": v.calcularVulnerabilidad(), "riesgo": v.calcularRiesgo()}
		catLogistica.append(jsonLogistica)

	for v in ventorno:
		avgvent += v.calcularVulnerabilidad()/ventorno.count()
		avgrent += v.calcularRiesgo()/ventorno.count()
		if v.encuesta.nombre not in encuestas_names:
			encuestas_names.append(v.encuesta.nombre)
			
		jsonEntorno = {"id": v.id, "nombre": v.encuesta.nombre, "vul": v.calcularVulnerabilidad(), "riesgo": v.calcularRiesgo()}
		catEntorno.append(jsonEntorno)

	sjson = {
		"papeletas": papeletas.count(),
		"papeletas_ids": p_ids,
		"v_infraestructura": avgvinfra,
		"r_infraestructura": avgrinfra,
		"v_seguridad_operativa": avgvsegop,
		"r_seguridad_operativa": avgrsegop,
		"v_seguridad_electronica": avgvsegelec,
		"r_seguridad_electronica": avgrsegelec,
		"v_logistica": avgvlogi,
		"r_logistica": avgrlogi,
		"v_entorno": avgvent,
		"r_entorno": avgrent,
		"cat_infraestructura": catInfraestructura,
		"cat_infraestructura_avg": getAVGVul(encuestas_names, catInfraestructura),
		"cat_seg_operativa": catSegop,
		"cat_seg_operativa_avg": getAVGVul(encuestas_names, catSegop),
		"cat_seg_electrica": catSegelc,
		"cat_seg_electrica_avg": getAVGVul(encuestas_names, catSegelc),
		"cat_logistica": catLogistica,
		"cat_logistica_avg": getAVGVul(encuestas_names, catLogistica),
		"cat_entorno": catEntorno,
		"cat_entorno_avg": getAVGVul(encuestas_names, catEntorno),

	} 

	return JsonResponse(sjson)

def getAVGVul(encuestas_names, cat):
	tempArray = []
	for name in encuestas_names:
		num = 0
		total = 0
		totalr = 0
		avg = 0
		avgr = 0
		for e in cat:
			if name == e["nombre"]:
				num += 1
				total += e["vul"]
				totalr += e["riesgo"]

		if num > 0:
			jsonTemp = {"nombre": name, "total": total, "totalr": totalr, "avg": (total/num), "avgr": (totalr/num) }
			tempArray.append(jsonTemp)

	return tempArray;
