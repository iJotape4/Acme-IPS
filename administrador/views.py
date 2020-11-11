#Importes de Renders Y Responses
from django.shortcuts import render

#Importes de utilidades

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Importes de métodos Triviales

#Importes de Modelos y Vistas
from administrador.models import Administrador

def menu_admin(request):
	return render(request, "./menu_Administrador.html")

def agregar_Medico(request):
	return render(request, "./registrar_Medico.html")

@method_decorator(csrf_exempt)
def agregarNuevoMedico(request):
	print(request.POST)
	pass