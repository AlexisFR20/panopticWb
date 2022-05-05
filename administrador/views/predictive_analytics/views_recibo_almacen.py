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
from querystring_parser import parser
from django.utils import timezone
from datetime import datetime
from django.core import serializers

# Estilos y JS común en vistas de administador
css_list =  ['basic', 'slick', 'metismenu', 'perfectscrollbar','custom-admin', 'custom-home', 'datatable-general', 'datatable-material', 'form-validator', 'daterangepicker', 'datepicker', 'wickedpicker', 'fancybox']
js_list   = ['js_basic', 'js_slick', 'js_metismenu', 'js_charts', 'js_perfectscrollbar', 'js-custom-home', 'js_datatables', 'js_form_validator', 'js_moment', 'js_daterangepicker', 'js_datepicker' ]



# Listado de Recibo Almacen - Historial
def admin_recibo_almacen_index(request):    
    recibo_almacen = RecibosAlmacen.objects.all()    
    
    return render(request, 'administrador/predictive/recibo_almacen/index.html', { 'css_list': css_list, 'js_list': js_list, 'recibo_almacen': recibo_almacen })

# Registro de Recibo Almacen - Crear
def admin_recibo_almacen_create(request):	
	recibo_almacen = RecibosAlmacen.objects.all()

	tipo_unidad = RecibosItems.TIPOUNIDAD
	#print(request.user.planta.id)
	# SI la forma fue enviada, se procesan los datos


	if request.method == 'POST':

		print(request.POST)
		
		try:

			recibo_almacen = RecibosAlmacen.objects.create(
				no_emp = request.POST['no_emp'],
				empleado = request.POST['empleado'],
				fecha = datetime.now(),
				departamento = request.POST['departamento'],
				jefe = request.POST['jefe'],
				turno = request.POST['turno'],
				planta = request.user.planta,
				user_aguilas = request.user,
				proveedor = request.POST['proveedor'],
				empresa = request.POST['empresa'],
				num_economico = request.POST['num_economico'],
				num_caja = request.POST['num_caja'],
			)
			recibo_almacen.save()
			
			post_dict = parser.parse(request.POST.urlencode())

			try:
				materiales = post_dict['materiales']
				 
				for material in materiales:
					recibos_items = RecibosItems.objects.create(
						recibo = recibo_almacen,
						cantidad = materiales[material]['cantidad'],
						unidad = materiales[material]['unidad'],
						desc = materiales[material]['desc'],
						noparte = materiales[material]['noparte'],
						origen = materiales[material]['origen'],
						destino = materiales[material]['destino'],
						fecha = datetime.now(),
						#fecha_salida = equipos[equi]['fecha_salida'],
					)
					recibos_items.save()


			except Exception as e_materiales:
				recibos_items = None

			messages.add_message(request,  messages.SUCCESS, 'El Registro ha sido registrado exitosamente')

		except Exception as e:
			recibo_almacen = None
			print(e)
			messages.add_message(request,  messages.ERROR, 'No se creo el registro correctamente, hubo un error.')
		
		return redirect('administrador:admin_recibo_almacen_index')
	else:
		return render(request, 'administrador/predictive/recibo_almacen/create.html', { 'css_list': css_list, 'js_list': js_list, 'recibo_almacen': recibo_almacen, 'tipo_unidad': tipo_unidad })

# Detalle de Recibo Almacen - Lista
def admin_recibo_almacen_show(request, pk):    
	recibo_almacen = RecibosAlmacen.objects.get(pk=pk)	

	try:
		print('hola')
		recibos_items = RecibosItems.objects.filter(recibo_id=recibo_almacen.id)
		print(recibos_items)
	except Exception:
		recibos_items = None	
	
	return render(request, 'administrador/predictive/recibo_almacen/show.html', { 'css_list': css_list, 'js_list': js_list, 'recibo_almacen': recibo_almacen, 'recibos_items': recibos_items })

# Detalle de Recibo Almacen - Lista
def admin_recibo_almacen_edit(request, pk):    
	recibo_almacen = RecibosAlmacen.objects.get(pk=pk)	
	tipo_unidad = RecibosItems.TIPOUNIDAD
	try:
		
		recibos_items = RecibosItems.objects.filter(recibo_id=recibo_almacen.id)
		
	except Exception:
		recibos_items = None	

	if request.method == 'POST':


		
		
		try:

			#print('Numero '+ )
			recibo_almacen.no_emp = request.POST['no_emp']
			recibo_almacen.empleado = request.POST['empleado']
			#recibo_almacen.fecha = datetime.now(),
			recibo_almacen.departamento = request.POST['departamento']
			recibo_almacen.jefe = request.POST['jefe']
			recibo_almacen.turno = request.POST['turno']
			#recibo_almacen.planta = request.user.planta
			#recibo_almacen.user_aguilas = request.user

			recibo_almacen.proveedor = request.POST['proveedor']
			recibo_almacen.empresa = request.POST['empresa']
			recibo_almacen.num_economico = request.POST['num_economico']
			recibo_almacen.num_caja = request.POST['num_caja']

			recibo_almacen.save()

			post_dict = parser.parse(request.POST.urlencode())

			try:
				materiales = post_dict['materiales']
			except Exception as e_material:
				materiales = None

			if materiales != None:	
				for material in materiales:

					if materiales[material]['id'] == 'new':
						recibos_items = RecibosItems.objects.create(
							recibo = recibo_almacen,
							cantidad = materiales[material]['cantidad'],
							unidad = materiales[material]['unidad'],
							desc = materiales[material]['desc'],
							noparte = materiales[material]['noparte'],
							origen = materiales[material]['origen'],
							destino = materiales[material]['destino'],
							fecha = datetime.now(),
							#fecha_salida = equipos[equi]['fecha_salida'],
						)
					else: 
						#print(materiales[material]['id'])
						#print(materiales[material]['desc'])
						recibos_items = RecibosItems.objects.get(pk=materiales[material]['id'])	
						recibos_items.recibo = recibo_almacen
						recibos_items.cantidad = materiales[material]['cantidad']
						recibos_items.unidad = materiales[material]['unidad']
						recibos_items.desc = materiales[material]['desc']
						recibos_items.noparte = materiales[material]['noparte']
						recibos_items.origen = materiales[material]['origen']
						recibos_items.destino = materiales[material]['destino']
						#fecha = datetime.now(),
				
					recibos_items.save()

			messages.add_message(request,  messages.SUCCESS, 'El Registro ha sido registrado exitosamente')
			return redirect('administrador:admin_recibo_almacen_index')

		except Exception as e_materiales:
			recibos_items = None
	
	return render(request, 'administrador/predictive/recibo_almacen/edit.html', { 'css_list': css_list, 'js_list': js_list, 'recibo_almacen': recibo_almacen, 'recibos_items': recibos_items, 'tipo_unidad': tipo_unidad })

# Detalle de Recibo Almacen - Lista
def admin_recibo_almacen_delete(request, pk):    
	try:
		go = RecibosAlmacen.objects.filter(id=pk).delete()
		messages.add_message(request,  messages.SUCCESS, 'Sucursal borrada exitosamente')
	except RecibosAlmacen.DoesNotExist:
		go = None        
		messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')

	return redirect('administrador:admin_recibo_almacen_index')

def admin_recibo_almacen_ajax_search(request): 
	id_rec_item = request.GET.get('id_rec_item')

	#if id_rec_item:
	#	obj_rec_item = RecibosItems.objects.get(pk=int(id_rec_item))
	#else:
	#	obj_rec_item = None

	try:
		go = RecibosItems.objects.filter(id=id_rec_item).delete()

		obj_rec_item = {
	        "Res": 'OK'
	    }

		#messages.add_message(request,  messages.SUCCESS, 'Sucursal borrada exitosamente')
	except RecibosAlmacen.DoesNotExist:
		go = None
		obj_rec_item = {
	        "Res": 'ERROR'
	    }        
		#messages.add_message(request,  messages.ERROR, 'No se borró la sucursal, probablemente no exista el id asociado')

	return JsonResponse(obj_rec_item, safe=False)