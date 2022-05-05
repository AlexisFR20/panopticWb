from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from analytics.models import Rondin, Punto, RondinHecho, PuntoHecho, EvidenciaPunto, F_18_puntos_Trailer, F_ES_Trailers
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
from analytics.models import *
# python -m pip install git+https://github.com/bernii/querystring-parser.git
from querystring_parser import parser
from django.utils import timezone
from datetime import datetime

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]

# Listado de Visitantes - Lista
def admin_visitantes_index(request):    
    f_visitantes = F_Visitantes.objects.all() 
    
    return render(request, 'administrador/predictive/visitantes_new/index.html', { 'css_list': css_list, 'js_list': js_list, 'f_visitantes': f_visitantes })

# Registro de Visitantes - Crear
def admin_visitantes_create(request):	
	f_visitantes = F_Visitantes.objects.all()

	#print(request.user.planta.id)
	# SI la forma fue enviada, se procesan los datos
	if request.method == 'POST':

		try:

			
			f_visitantes = F_Visitantes.objects.create(
				planta = request.user.planta,
				tipo = request.POST['tipo'],
				nombre = request.POST['nombre'],
				empresa = request.POST['empresa'],
				anfitrion = request.POST['anfitrion'],
				confirmo_anfitrion = request.POST['confirmo_anfitrion'],
				identificacion = request.POST['identificacion'],
				gafete = request.POST['gafete'],
				#placas = request.POST['placas'],
				entrada = datetime.now()
				#salida = request.POST['salida']
			)
			f_visitantes.save()
			

			if request.POST['marca'] != None or request.POST['modelo'] != None or request.POST['placas'] != None or request.POST['nota'] != None:
				print('vehiculo re')
				
				entrada_vehiculo = EntradaVehiculo.objects.create(
					visitante = f_visitantes,
				    planta = request.user.planta,
				    #fecha = request.POST['fecha'],
				    guardia = request.user,
				    marca = request.POST['marca'],
				    modelo = request.POST['modelo'],
				    placas = request.POST['placas'],
				    nota = request.POST['nota']
				)
				entrada_vehiculo.save()
				
			
			post_dict = parser.parse(request.POST.urlencode())

			try:
				equipos = post_dict['equipo']

				entrada_equipo = EntradaEquipo.objects.create(
					visitante = f_visitantes,
					planta = request.user.planta,
					#fecha = 
					guardia = request.user,
					nombre = request.POST['nombre']
				)
				entrada_equipo.save()

				for equi in equipos:

					item_entrada_equipo = ItemEntradaEquipo.objects.create(
						entradaequipo = entrada_equipo,
						descripcion = equipos[equi]['nombre_equipo'],
						n_serie = equipos[equi]['num_serie_equipo'],
						cantidad = equipos[equi]['cantidad_equipo']
					)
					item_entrada_equipo.save()

			except Exception as e_equipo:
				equipos = None

			print('*******')

			try:
				materiales = post_dict['material']				
				
				entrada_materiales = EntradaMateriales.objects.create(
					visitante = f_visitantes,
					planta = request.user.planta,
					#fecha = 
					guardia = request.user,
					nombre = request.POST['nombre']
				)
				entrada_materiales.save()

				

				for mat in materiales:

					item_entrada_material = ItemEntradaMaterial.objects.create(
						entradamateriales = entrada_materiales,
						descripcion = materiales[mat]['descripcion_material'],
						tipo = materiales[mat]['tipo_material']
					)
					item_entrada_material.save()
			except Exception as e_materiales:
				materiales = None
		    
			
			
			messages.add_message(request,  messages.SUCCESS, 'Visitante ha sido registrado exitosamente')



		except Exception as e:
			f_visitantes = None
			print(e)
			messages.add_message(request,  messages.ERROR, 'No se creo el registro correctamente, hubo un error.')
		return redirect('administrador:admin_visitantes_index')
	else:
		return render(request, 'administrador/predictive/visitantes_new/create.html', { 'css_list': css_list, 'js_list': js_list, 'f_visitantes': f_visitantes })

# Listado de Visitantes - Lista
def admin_visitantes_show(request, pk):    
	visitante = F_Visitantes.objects.get(pk=pk)

	try:
		vehiculo = EntradaVehiculo.objects.get(visitante=visitante)
	except Exception:
		vehiculo = None

	try:
		equipos = EntradaEquipo.objects.get(visitante=visitante)
	except Exception:
		equipos = None

	try:
		ItemsEquipos = ItemEntradaEquipo.objects.filter(entradaequipo_id=equipos.id)
	except Exception:
		ItemsEquipos = None

	try:
		materiales = EntradaMateriales.objects.get(visitante=visitante)
	except Exception:
		materiales = None	
	    
	try:
		ItemsMateriales = ItemEntradaMaterial.objects.filter(entradamateriales_id=materiales.id)	
	except Exception:
		ItemsMateriales = None	
	
	return render(request, 'administrador/predictive/visitantes_new/show.html', { 'css_list': css_list, 'js_list': js_list, 'visitante': visitante, 'vehiculo': vehiculo, 'equipos': equipos, 'ItemsEquipos':ItemsEquipos, 'materiales': materiales, 'ItemsMateriales': ItemsMateriales })
