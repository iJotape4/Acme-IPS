from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
from django.template.loader import get_template
from mysql.connector import errorcode
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from GestionDeCitas.models import Cita, Paciente
from Software2.Methods import EliminarSimbolos, CursorDB, GenerateUserByCorreoElement, send_email
from Autenticacion.views import nombre as nombreUsuarioViews
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt)
def principal(request):
	request.session.flush() #Elimina la sesion actual --> django.session en la bd
	nombreUsuarioViews = None #con el fin de evitar que cierre sesion y cuando le de regresar pagina, siga en la sesion
	print("-Sesion finalizada-")
	print(nombreUsuarioViews)
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

	'''cita = Cita.objects.filter(PacienteConCita_id) and Cita.objects.filter(MotivoConsultaCita) and Cita.objects.filter(HorarioCita) '''
	cita = Cita.objects.all()
	print(cita)
	citas = []
	for a in cita:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita.time, 'motivo': a.MotivoConsultaCita}
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

def menu_Paciente(request):

    return render(request, "./menu_Paciente.html")

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