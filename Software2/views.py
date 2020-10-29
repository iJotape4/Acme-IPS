#Importes de Renders Y Responses
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

#Importes de Utilidades Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

#Importes de utilidades
import mysql.connector
from mysql.connector import errorcode
import datetime

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

#Importes de Modelo Y vistas
from GestionDeCitas.models import Cita, Paciente
from Autenticacion.views import get_nombreUsuario, set_nombreUsuario, get_is_logged_in, set_is_logged_in

#Importes de métodos triviales
from Software2.Methods import EliminarSimbolos, CursorDB, GenerateUserByCorreoElement, send_email

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

cnx = mysql.connector.connect(user='root', password='Sistemas132',host='127.0.0.1',database='dbipsacme')
class Paciente(object):
	def __init__(self, nombreCompleto, horaCita):
		self.nombreCompleto = nombreCompleto
		#self.apellido = apellido
		self.horaCita = horaCita

class doctor(object):
	def __init__(self, nombre, apellido):
		self.nombre = nombre
		self.apellido = apellido

def citas_del_dia(request):
	cita = Cita.objects.filter(DiaCita=timezone.now())
	print(cita)
	citas = []
	for a in cita:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita}
		citas.append(list_Cita)

	return render(request, "./citas_del_dia.html",{"lista":citas})

def correo(request):
	if request.method == 'POST':
		mail = request.POST.get('mail')
		User = GenerateUserByCorreoElement(mail)
		send_email(mail, User[0], User[1], "./correo.html" )
		
	return render(request, "./regisCorreo.html")

lista = [1,2,3,4]
def histo_Paciente(request):
	
	return render(request, "./histo_Paciente.html", {"lista":lista})

def vistaDoctor(request):
	
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
	ahora = datetime.datetime.now()
	
	#Define un diccionario con lo que será necesario para mostrarse en el html
	diccionario = {"nombre_doctor":D1.nombre, "apellido_doctor":D1.apellido, "Hoy":ahora, "pacientes":pacientes}

	#Devuelve el html y el diccionario 
	return render(request, 'PlantillaDoctor.html', diccionario ) 