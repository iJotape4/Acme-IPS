#Importes de Renders Y Responses
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from twilio.rest import Client 

#Importes de Utilidades Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

#Importes de utilidades
import mysql.connector
from mysql.connector import errorcode
from datetime import date, datetime, time, timedelta

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

#Importes de métodos triviales
from Software2.Methods import EliminarSimbolos, CursorDB, GenerateUserByCorreoElement, send_email

#Importes de Modelos y Vistas
from GestionDeCitas.models import Cita, Paciente, Especialidad, Medico
from Autenticacion.views import get_nombreUsuario, set_nombreUsuario, get_is_logged_in, set_is_logged_in

def menu_secretaria(request):
	return render(request, "menu_secretaria.html")

def informe_secretaria(request):
	citas= Cita.objects.filter(DiaCita=(datetime.now()+ timedelta(days=1)).date())
	lista=[]
	for a in citas:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita, 'numero' :a.PacienteConCita.Telefono}
		lista.append(list_Cita)
	return render(request, "informe_secretaria.html",{"lista":lista})

@never_cache
@method_decorator(csrf_exempt)
def principal(request):
	print("Request principal: ",request.POST)
	print("Logout usuario: {} ---- is logged in: {}".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")
	request.session.flush() #Elimina la sesion actual --> django.session en la bd
	set_is_logged_in(None)
	set_nombreUsuario(None)
	print("|-- Sesion finalizada: {} | Sesion: {} --|".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")
	return render(request,"principalPage.html")

def enviarWssp(numero_telefono,nombre_paciente,nombre_medico,fecha_cita,hora_cita): 
	#Para unir a otro usuario al SandBox usar este link
	#whatsapp://send?phone=<Your Sandbox Number>&text=<your URL-encoded sandbox keyword>
	#<Your Sandbox Number> = el numero de from_='whatsapp:
	#<your URL-encoded sandbox keyword> = el codigo de cada Sandbox, en el caso de SandBox de Jhoan el codigo es -> join interest-birth

	#SandBox de Jhoan
	account_sid = 'AC4e8a7439bca57265e706ebde409569c7' 
	auth_token = 'b5edd4064f72c69d4fe8be77cbf26f48' 
	client = Client(account_sid, auth_token) 
	
	message = client.messages.create(
		from_='whatsapp:+14155238886',
		body='Hola {} bienvenido a IPS ACME, Tu salud es nuestra prioridad, recuerda que tu cita ha sido agendada para la fecha {} , hora {} , con el médico {}'.format(nombre_paciente,fecha_cita,hora_cita,nombre_medico),    
		to='whatsapp:+57'+str(numero_telefono)
	) 
	print("\n")
	print(message.sid)
	print("\n")

	#SandBox de Yesid
	'''account_sid = 'AC02921a0384fd5426276893a7ee00b421' 
	auth_token = 'ad1d1bc3043001edfe9bc2cbd8daaadc' 
	client = Client(account_sid, auth_token)     
	message = client.messages.create( from_='whatsapp:+14155238886', body='Esto no es un virus xDD',to='whatsapp:+573165634347')     
	print(message.sid)'''

def correo(request):
	if request.method == 'POST':
		mail = request.POST.get('mail')
		User = GenerateUserByCorreoElement(mail)
		send_email(mail, User[0], User[1], "./correo.html")
	return render(request, "./regisCorreo.html")


	
#FORMA DE HACER CONSULTAS USANDO QUERY SETS DE SQL
cnx = mysql.connector.connect(user='root', password='Sistemas132',host='127.0.0.1',database='dbipsacme')

def MétodoQuerysSQL(request):

	cursor= CursorDB(cnx)
	
	#Consulta para buscar	 el nombreCompleto de los pacientes
	query = ("SELECT PrimerNombreP, SegundoNombreP, PrimerApellidoP, SegundoApellidoP FROM paciente")
	#(¿¿)Agregar WHERE cita.día = Today (??)
	 
	consulta = cursor.execute(query)	
	pacientes =[]

	for i in cursor:
		P1= Paciente(EliminarSimbolos(i),"10:00 ")
		pacientes.append(P1)		
	#Declara un objeto Doctor
	D1 =doctor("Miguel","Lizarazo")
	ahora = datetime.now()
	
	#Define un diccionario con lo que será necesario para mostrarse en el html
	diccionario = {"nombre_doctor":D1.nombre, "apellido_doctor":D1.apellido, "Hoy":ahora, "pacientes":pacientes}

	#Devuelve el html y el diccionario 
	return render(request, 'PlantillaDoctor.html',diccionario)