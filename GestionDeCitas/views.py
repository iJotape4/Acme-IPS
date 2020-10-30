#Importes de Renders Y Responses
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

#Importes de utilidades
from django.contrib import messages
from django import forms

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Importes de métodos Triviales
from Software2.Methods import send_email, GenerarHorarioCitas, FormatFecha

#Importes de Modelos y Vistas
from GestionDeCitas.models import Paciente, Medico,Horario,Especialidad,Cita
from GestionDeCitas.forms import AgendarCitaForm
from Autenticacion.views import login, get_nombreUsuario, get_is_logged_in, get_idUsuario

class AgendarCitaView(TemplateView):
    template_name = 'agendamiento_Citas.html'
    especialidad_AJAX = ""
    medico_AJAX = ""
    horario_AJAX = ""

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
            respuesta = list(request.POST.values())
            action = respuesta[0]
            if action == 'buscar_medico_por_especialidad':
                data = AgendarCitaView.filtrar_Medicos(self,data,respuesta)
            elif action == 'buscar_horario_por_medico':
                data = AgendarCitaView.filtrar_Horarios(self,data,respuesta)
            elif action == 'seleccionar_horario':
                AgendarCitaView.horario_AJAX = respuesta[1]
                print("Horario AJAX: ",AgendarCitaView.horario_AJAX)
            else:   
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data,safe=False)

    def filtrar_Medicos(self,data,respuesta):
       
        #print("\n Filtrar Medicos")
        #print(respuesta)
        #print("\n")
        especialidad = respuesta[1]
        AgendarCitaView.especialidad_AJAX = especialidad

        especialidad_AJAX = especialidad
        id_especialidad_Escogida = list(Especialidad.objects.filter(nombre=especialidad).values_list('id',flat=True))
        
        filtro = list(Medico.objects.filter(especialidad_id=id_especialidad_Escogida[0]).values())
        for dato in filtro:
            data.append({'PrimerNombre': dato['PrimerNombre'],'PrimerApellido':dato['PrimerApellido']})
        return data

    def filtrar_Horarios(self,data,respuesta):
        #print("\n Filtrar horarios")
        #print(respuesta)
        #print("\n")
        medico = respuesta[1]
        AgendarCitaView.medico_AJAX = medico

        medicoElegido = str(medico).split()

        id_Horario_Escogido = list(Medico.objects.filter(PrimerNombre=medicoElegido[0], PrimerApellido=medicoElegido[1]).values_list('horario_id',flat=True))
        print(id_Horario_Escogido)
        filtro = list(Horario.objects.filter(id=id_Horario_Escogido[0]).values())
        
        particion_horarios = GenerarHorarioCitas(filtro[0]['HorarioLlegada'],filtro[0]['HoraioSalida'])
        for date in particion_horarios:
            data.extend([{"Horarios":date}])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AgendarCitaForm()
        return context

@method_decorator(csrf_exempt)
def AgendarCita(request):

    print("\n")
    print("Usuario agendamiento: ",get_nombreUsuario())
    print("\n")
    ModalidadCita = request.POST.get("tipoCita") 
    MotivoConsulta = request.POST.get("motivo_consulta" )
    fecha = FormatFecha(request.POST.get("fecha" ))

    EspecialidadC =list(Especialidad.objects.filter(nombre= request.POST.get("especialidades")).values_list('id',flat=True))[0]

    medicoElegido = str(request.POST.get("medicos" )).split()

    MedicoC =list(Medico.objects.filter(PrimerNombre=medicoElegido[0], PrimerApellido=medicoElegido[1] ).values_list('id',flat=True))[0]
    
    HorarioC = AgendarCitaView.horario_AJAX 

    PacienteConCita = Paciente.objects.filter(DocumentoId=get_idUsuario()).values_list('id',flat=True)[0]

    #Se pasa reporte por defecto ya que aún no se puede validar
    Cita.objects.create(ModalidadCita=ModalidadCita, MotivoConsultaCita=MotivoConsulta,
    Especialidad_id=EspecialidadC,HorarioCita= HorarioC, MedicoAsignado_id= MedicoC,
    PacienteConCita_id=PacienteConCita, ReporteSec_id=1, DiaCita=fecha)
    return render(request,'menu_Paciente.html',{"userlogeado":get_nombreUsuario(),'logeado':request.session['usuario']})
    
