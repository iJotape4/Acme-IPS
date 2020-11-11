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
from GestionDeCitas.models import Medico, Horario, Especialidad
from administrador.forms import AgregarMedicoForm

class AgregarMedicoView(TemplateView):
    template_name = 'registrar_Medico.html'
    especialidad_AJAX = ""

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AgregarMedicoForm()
        return context

@method_decorator(csrf_exempt)
def AgregarMedico(request):
    
    print("\n")
    print(request.POST)
    print("\n")
    primerNombre = request.POST.get('pri_Nombre_Med')
    segundoNombre = request.POST.get('seg_Nombre_Med')
    primerApellido = request.POST.get('pri_Apellido_Med')
    segundoApellido = request.POST.get('seg_Apellido_Med')
    documentoId = request.POST.get('Documento_Id')
    edad = request.POST.get('edad')
    correoElectronico = request.POST.get('email')
    tipoDocumento = request.POST.get('tipo_documento')
    usuario = request.POST.get('username')
    contraseña = request.POST.get('password')
    horarioEntrada = request.POST.get('horario_Entrada')
    horarioSalida = request.POST.get('horario_Salida')
    
    especialidad_id = Especialidad.objects.filter(
        nombre=request.POST.get('especialidades')
        ).values_list(
            'id',flat=True
        )[0]
    """print("\n")
    print("Especialidad ID: ",especialidad_id)
    print("Horario Entrada: ",horarioEntrada)
    print("Horario Salida: ",horarioSalida)
    print("\n")"""

    """ <QueryDict: {'csrfmiddlewaretoken': ['a1qR880OieEL0QyNYJBYiGb8uQsJmoPoPtyNBrlYrFl0HEZsBjN5a4TDmijo3uxg'], 
    'pri_Nombre_Med': ['juan'], 'seg_Nombre_Med': ['jimenez'], 'pri_Apellido_Med': ['quesada'], 
    'seg_Apellido_Med': ['carreño'], 'edad': ['13'], 'tipo_documento': ['CC'], 
    'Documento_Id': ['1005742'], 'especialidades': ['doctorhouse'], 'email': ['sadwqe@hotmail.com'], 
    'horario_Entrada': ['08:30'], 'horario_Salida': ['17:04'], 'username': ['Pepito'], 'password': ['123']}>
    """

    horarioAgregado = Horario.objects.create(HorarioLlegada=horarioEntrada,HoraioSalida=horarioSalida)
    
    horario_id = Horario.objects.filter(
        HorarioLlegada=horarioEntrada,
        HoraioSalida=horarioSalida
        ).values_list('id',flat=True)[0]
    
    """print("\n")
    print("Horario creado ID: ",horario_id)
    print("\n")"""
    medicoAgregado = Medico.objects.create(PrimerNombre=primerNombre, SegundoNombre=segundoNombre, 
        PrimerApellido=primerApellido, SegundoApellido=segundoApellido, DocumentoId=documentoId,
        Edad=edad, CorreoElectronico=correoElectronico, TipoUsuario='Medico',
        TipoDocumento=tipoDocumento,Usuario=usuario,Contraseña=contraseña,
        especialidad_id=especialidad_id,horario_id=horario_id)
    return render(request, "./menu_Administrador.html")

def menu_admin(request):
	return render(request, "./menu_Administrador.html")

