#Importes de Renders Y Responses
from django.shortcuts import render

#Importes de utilidades

#Importes de decoradores

#Importes de métodos Triviales

#Importes de Modelos y Vistas
from administrador.models import Administrador



def menu_admin(request):

	return render(request, "./menu_Administrador.html")

def agregar_Medico(request):

	return render(request, "./registrar_Medico.html")
