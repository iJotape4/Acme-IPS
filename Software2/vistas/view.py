from django.http import HttpResponse
from django.shortcuts import render
import mysql.connector
from mysql.connector import errorcode
import datetime
from Software2.Methods import EliminarSimbolos, CursorDB

cnx = mysql.connector.connect(user='root', password='Sistemas132',host='127.0.0.1',database='dbipsacme')
class Paciente(object):
	def __init__(self, nombre, apellido, horaCita):
		self.nombre = nombre
		self.apellido = apellido
		self.horaCita = horaCita

class doctor(object):
	def __init__(self, nombre, apellido):
		self.nombre = nombre
		self.apellido = apellido

def login(request):

    return render(request,"./login.html")

def registro(request):

    return render(request, "./registro.html")

def vistaDoctor(request):
	
	cursor= CursorDB(cnx)

	query = ("SELECT PrimerNombreP, SegundoNombreP, PrimerApellidoP, SegundoApellidoP FROM paciente")

	consulta = cursor.execute(query)	
	pacientes =[]

	for i in cursor:
		pacientes.append(EliminarSimbolos(i))

	#Declara un objeto Doctor
	D1 =doctor("Miguel","Lizarazo")
	ahora = datetime.datetime.now()
	
	#Define un diccionario con lo que será necesario para mostrarse en el html
	diccionario = {"nombre_doctor":D1.nombre, "apellido_doctor":D1.apellido, "Hoy":ahora, "pacientes":pacientes}

	#Devuelve el html y el diccionario 
	return render(request, 'PlantillaDoctor.html', diccionario )  