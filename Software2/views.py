from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from twilio.rest import Client 

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from datetime import date, datetime, time, timedelta

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from Software2.Methods import EliminarSimbolos, GenerateUserByCorreoElement, send_email

from GestionDeCitas.models import Cita, Paciente, Especialidad, Medico
from Autenticacion.views import get_nombreUsuario, set_nombreUsuario, get_is_logged_in, set_is_logged_in

def menu_secretaria(request):
	return render(request, "menu_secretaria.html")


@never_cache
@method_decorator(csrf_exempt)
def principal(request):
	print("Request principal: ",request.POST)
	print("Logout usuario: {} ---- is logged in: {}".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")
	request.session.flush()
	set_is_logged_in(None)
	set_nombreUsuario(None)
	print("|-- Sesion finalizada: {} | Sesion: {} --|".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")
	return render(request,"principalPage.html")

def enviarWssp(numero_telefono,nombre_paciente,nombre_medico,fecha_cita,hora_cita): 

	account_sid = 'AC4e8a7439bca57265e706ebde409569c7' 
	auth_token = 'b5edd4064f72c69d4fe8be77cbf26f48' 
	client = Client(account_sid, auth_token) 
	
	message = client.messages.create(
		from_='whatsapp:+14155238886',
		body='Hola {} bienvenido a IPS ACME, Tu salud es nuestra prioridad, recuerda que tu cita ha sido agendada para la fecha {} , hora {} , con el médico {}'.format(nombre_paciente,fecha_cita,hora_cita,nombre_medico),    
		to='whatsapp:+57'+str(numero_telefono)
	) 


def correo(request):
	if request.method == 'POST':
		mail = request.POST.get('mail')
		User = GenerateUserByCorreoElement(mail)
		send_email(mail, User[0], User[1], "./correo.html")
	return render(request, "./regisCorreo.html")
