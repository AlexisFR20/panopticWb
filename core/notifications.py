from django.shortcuts import render, HttpResponse
from django.core.mail import send_mail
import requests
from django.urls import reverse, reverse_lazy
from core import notifications
from core.models import User, Notificacion

def sendNotification(title, body, token, email):


	url = 'https://fcm.googleapis.com/fcm/send'
	headers = { 'Content-Type': 'application/json', 'Authorization': 'key=AAAAdrWypJs:APA91bFMgOWVCk4QdMScx8u8nMQxkO1T-QuELLpPkBusiH54jRkZD0Fx2zVZ90dlAgYVDwog0WzH-Z6vWICElx2fD0fLSOa67jkqp3vlM4BltTcw7DfuHmYKfIIPyNdIailwXT31jvQX'}
	payload = { 'to': token, "notification": {"title": title, "body": body} }

	response = requests.post(url, json=payload, headers=headers)
	
	print(response.content)

	send_mail(title, body, email, [email], fail_silently=False)


	return HttpResponse('ok')

def sendNotification(title, body, token, email, noti):


	url = 'https://fcm.googleapis.com/fcm/send'
	headers = { 'Content-Type': 'application/json', 'Authorization': 'key=AAAAdrWypJs:APA91bFMgOWVCk4QdMScx8u8nMQxkO1T-QuELLpPkBusiH54jRkZD0Fx2zVZ90dlAgYVDwog0WzH-Z6vWICElx2fD0fLSOa67jkqp3vlM4BltTcw7DfuHmYKfIIPyNdIailwXT31jvQX'}
	payload = { 'to': token, "notification": {"title": title, "body": body} }

	response = requests.post(url, json=payload, headers=headers)
	
	print(response.content)
	
	body2 = body

	if noti.idproblema != None:
		if noti.modelo == "Movimiento":
			body2 += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_movimientos_detalle', kwargs={'pk': noti.idproblema})
		if noti.modelo == "Incidentes":
			body2 += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_incidentes_servicio_lista')
		if noti.modelo == "EstadoFuerza":
			body2 += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_estados_fuerza')
		if noti.modelo == "Papeleta":
			body2 += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_papeleta_detalle', kwargs={'id': noti.idproblema})
		if noti.modelo == "RondinHecho":
			body2 += "\n\n http://panoptic.iottechnologies.mx"+reverse('analytics:rondinhecho_detalle', kwargs={'id': noti.idproblema})
			
	send_mail(title, body2, email, [email], fail_silently=False)


	return HttpResponse('ok')

def sendemailsbyplanta(title, body, planta, modulo, noti):
		
		if modulo == "predictive":
			emails = planta.mails_predictive
			print("emails="+str(emails))
			if emails != "" and emails != None:
				emails = emails.replace(", ", ",")
				emailsarray = emails.split(",");
				print(emails)
				if noti.modelo == "Incidentes":
					print(noti.modelo)
					body += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_incidentes_servicio_lista')
				if noti.modelo == "EstadoFuerza":
					body += "\n\n http://panoptic.iottechnologies.mx"+reverse('analytics:estados_fuerza')
				if noti.modelo == "RondinHecho":
					print(noti.modelo)
					body += "\n\n http://panoptic.iottechnologies.mx"+reverse('analytics:rondinhecho_detalle', kwargs={'id': noti.idproblema})

		if modulo == "zona0":
			emails = planta.mails_zona
			print("emails="+str(emails))
			if emails != "" and emails != None:
				emails = emails.replace(", ", ",")
				emailsarray = emails.split(",");
				print(emails)

		if modulo == "ddmanagement":
			emails = planta.mails_dd
			print("emails="+str(emails))
			if emails != "" and emails != None:
				emails = emails.replace(", ", ",")
				emailsarray = emails.split(",");
				print(emails)
				if noti.modelo == "Movimiento":
					print(noti.modelo)
					body += "\n\n http://panoptic.iottechnologies.mx"+reverse('ddmanagement:admin_movimientos_detalle', kwargs={'pk': noti.idproblema})

		if modulo == "arnes":	
			emails = planta.mails_analisis_riesgo
			print("emails="+str(emails))
			if emails != "" and emails != None:
				emails = emails.replace(", ", ",")
				emailsarray = emails.split(",");
				print(emails)
				if noti.modelo == "Papeleta":
					print(noti.modelo)
					body += "\n\n http://panoptic.iottechnologies.mx"+reverse('administrador:admin_papeleta_detalle', kwargs={'id': noti.idproblema})

		send_mail(title, body, "admin@grupoaguilas.com", emailsarray, fail_silently=False)

		for email in emailsarray:
			print("buscar email "+email)
			user = User.objects.filter(email=email).first()
			if(user != None):
				print("encontrado")
				notificacion = Notificacion()
				notificacion.titulo = noti.titulo
				notificacion.mensaje = noti.mensaje
				notificacion.modelo = noti.modelo
				notificacion.idproblema = noti.idproblema
				notificacion.param_bol = noti.param_bol
				notificacion.usuario_id = user.id
				notificacion.save()