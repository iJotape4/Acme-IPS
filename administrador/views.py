
from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse

from django import forms

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from administrador.models import Administrador
from GestionDeCitas.models import Medico, Horario, Especialidad
from administrador.forms import AgregarMedicoForm

class AgregarMedicoView(TemplateView):
    template_name = 'registrar_Medico.html'
    especialidad_AJAX = ""

    @method_decorator(csrf_exempt)
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

    horarioAgregado = Horario.objects.create(HorarioLlegada=horarioEntrada,HoraioSalida=horarioSalida)
    
    horario_id = Horario.objects.filter(
        HorarioLlegada=horarioEntrada,
        HoraioSalida=horarioSalida
        ).values_list('id',flat=True)[0]
    
    medicoAgregado = Medico.objects.create(PrimerNombre=primerNombre, SegundoNombre=segundoNombre, 
        PrimerApellido=primerApellido, SegundoApellido=segundoApellido, DocumentoId=documentoId,
        Edad=edad, CorreoElectronico=correoElectronico, TipoUsuario='Medico',
        TipoDocumento=tipoDocumento,Usuario=usuario,Contraseña=contraseña,
        especialidad_id=especialidad_id,horario_id=horario_id)
    return render(request, "./menu_Administrador.html")

def menu_admin(request):
	return render(request, "./menu_Administrador.html")

