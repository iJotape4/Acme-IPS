#Importes de Renders Y Responses
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

#Importes de utilidades
from django import forms

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Importes de métodos Triviales

#Importes de Modelos y Vistas
from administrador.models import Administrador
from administrador.forms import AgregarMedicoForm

class AgregarMedicoView(TemplateView):
    template_name = 'registrar_Medico.html'
    especialidad_AJAX = ""

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        print("\n")
        print("Haciendo POST -> ",request.POST)
        print("\n")
        try:
           pass
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data,safe=False)



def get_context_data(self, **kwargs):
	context = super().get_context_data(**kwargs)
	context['form'] = AgregarMedicoForm()
	return context


def menu_admin(request):

	return render(request, "./menu_Administrador.html")

def agregar_Medico(request):

	return render(request, "./registrar_Medico.html")
