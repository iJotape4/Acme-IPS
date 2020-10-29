from django.shortcuts import render

def menu_admin(request):

	return render(request, "./menu_Administrador.html")

def agregar_Medico(request):

	return render(request, "./registrar_Medico.html")
