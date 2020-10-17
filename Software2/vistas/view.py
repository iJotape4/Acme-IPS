from django.http import HttpResponse
from django.template import loader
import datetime

class Paciente(object):
	def __init__(self, nombre, apellido, horaCita):
		self.nombre = nombre
		self.apellido = apellido
		self.horaCita = horaCita

class doctor(object):
	def __init__(self, nombre, apellido):
		self.nombre = nombre
		self.apellido = apellido

def saludo(request):

    return HttpResponse("<html><body><h1>Hola mundo</h1></body></html>")

def despedida(request):

    return HttpResponse("<html><body><h1>El programa se despide</h1></body></html>")

def paginaPrincipal(request):

    return HttpResponse("<html><body><h1>Bienvenidos a ACME!!</h1></body></html>")

def vistaDoctor(request):
	#Declara un objeto Doctor
	D1 =doctor("Miguel","Lizarazo")

	#Declara varios pacientes y crea una lista
	p1 =Paciente("Juan","Perez","08:00")
	p2 =Paciente("Esteban","Florez","08:20")
	p3 =Paciente("Daniel","Lopez","09:00")
	p4 =Paciente("Jhoan","Ortiz","10:00")
	p5 =Paciente("Javier","Parra","11:00")

	pacientes =[p1, p2, p3, p4, p5]

	#Carga el html con la vista del doctor del directorio de vistas
	plantilla_Doctor = loader.get_template('PlantillaDoctor.html')

	ahora = datetime.datetime.now()
	
	#Define un diccionario con lo que será necesario para mostrarse en el html
	diccionario = {"nombre_doctor":D1.nombre, "apellido_doctor":D1.apellido, "Hoy":ahora, "pacientes":pacientes}

	#Renderiza el html con los valores del diccionario
	doctorView = plantilla_Doctor.render(diccionario)

	#Devuelve el html renderizado
	return HttpResponse(doctorView)    