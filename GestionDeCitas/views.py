#Importes de Renders Y Responses
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

#Importes de utilidades
from django.contrib import messages
from django import forms
from datetime import time

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

#Importes de métodos Triviales
from Software2.Methods import send_email, GenerarHorarioCitas, FormatFecha, DiscardMedicsWhit12Citas, CitaSinRealizar
from Software2.Methods import pdf_Generator_Cita, send_emailPdfQr
from Software2.views import enviarWssp

#Importes de Modelos y Vistas
from GestionDeCitas.models import Paciente, Medico,Horario,Especialidad,Cita, ReporteSecretaria
from GestionDeCitas.forms import AgendarCitaForm
from Autenticacion.views import login, get_nombreUsuario, get_is_logged_in, get_idUsuario

class AgendarCitaView(TemplateView):
    template_name = 'agendamiento_Citas.html'
    especialidad_AJAX = ""
    medico_AJAX = ""
    horario_AJAX = ""
    fecha_AJAX =""

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
            elif action == 'fecha_escogida':
                AgendarCitaView.fecha_AJAX = respuesta[1]
                print("fecha_AJAX: ",AgendarCitaView.fecha_AJAX)
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
        print("fechaza")
        print(AgendarCitaView.fecha_AJAX)

        particion_medicos =DiscardMedicsWhit12Citas(filtro, FormatFecha(AgendarCitaView.fecha_AJAX))

        for dato in particion_medicos:
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
        
        particion_horarios = GenerarHorarioCitas(filtro[0]['HorarioLlegada'],filtro[0]['HoraioSalida'], medicoElegido, FormatFecha(AgendarCitaView.fecha_AJAX))
    
        #Hacer un Warning para cuando ya se asignaron todos los horarios:
        for date in particion_horarios:
            data.extend([{"Horarios":date}])
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AgendarCitaForm()
        return context

@method_decorator(csrf_exempt)
def AgendarCita(request):
    try:
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

        Reporte = ReporteSecretaria.objects.filter(FechaReporte=fecha).values_list('id',flat=True)

        if Reporte:
            ReporteSec = Reporte[0]
        else:
            ReporteSecretaria.objects.create(FechaReporte=fecha)
            ReporteSec = ReporteSecretaria.objects.filter(FechaReporte=fecha).values_list('id',flat=True)[0]

        try:
            
            citaCreada = Cita.objects.create(ModalidadCita=ModalidadCita, MotivoConsultaCita=MotivoConsulta,
            Especialidad_id=EspecialidadC,HorarioCita= HorarioC, MedicoAsignado_id= MedicoC,
            PacienteConCita_id=PacienteConCita, ReporteSec_id=ReporteSec, DiaCita=fecha
            )

            whatsAppPacienteConCita = Paciente.objects.filter(DocumentoId=get_idUsuario()).values_list('Whatsapp',flat=True)[0]
            respuesta = pdf_Generator_Cita(request,citaCreada)
            print("modalidadCita: ",ModalidadCita)
            if ModalidadCita=='virtual':
                virtual = 'Este es el link para tu cita modalidad virtual: https://meet.google.com/_meet/uqv-szki-gbu?ijlm=1604973501889&hs=130'
                send_emailPdfQr(respuesta[0],"./correoPdfCita.html",respuesta[1],whatsAppPacienteConCita,virtual)
            else:
                send_emailPdfQr(respuesta[0],"./correoPdfCita.html",respuesta[1],whatsAppPacienteConCita,'')
            
            enviarWssp(whatsAppPacienteConCita,get_nombreUsuario(),
            AgendarCitaView.medico_AJAX,AgendarCitaView.fecha_AJAX,
            AgendarCitaView.horario_AJAX
            )
        except Exception as e:
            messages.warning(request,'No se ha podido agendar tu cita, revisa los datos del formulario')
            print("Ha ocurrido un error al agendar la cita {}".format(e))
        finally:
            return render(request,'menu_Paciente.html',{"userlogeado":get_nombreUsuario(),'logeado':request.session['usuario']})
    except Exception as e:
        messages.warning(request,'No se ha podido agendar tu cita, revisa los datos del formulario')
        print("Ha ocurrido un error al agendar la cita {}".format(e))
    finally:
        return render(request,'menu_Paciente.html',{"userlogeado":get_nombreUsuario(),'logeado':request.session['usuario']})

def reagendarSecretaria(request):
    return render(request,'reagendar_secretaria.html')

def reagendarPaciente(request):
    return render(request,'reagendar_paciente.html')

def histo_Paciente(request):
    paciente = Paciente.objects.filter(DocumentoId=get_idUsuario())[0]
    citasPaciente = Cita.objects.filter(PacienteConCita=paciente.id).order_by('DiaCita')
    lista = []
    for a in citasPaciente:
        list_Cita = {'medico':"%s %s" %(a.MedicoAsignado.PrimerNombre, a.MedicoAsignado.PrimerApellido),
        'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita,
        'fecha': a.DiaCita, 'asistencia':a.Asistencia, 'especialidad':a.Especialidad.nombre,
        'programada': CitaSinRealizar(a.DiaCita, a.HorarioCita)   
        }
        lista.append(list_Cita)
    return render(request,"./histo_Paciente.html", {"lista":lista})


#################### Agendar Secretaria

def buscarPacienteCC(request):
    return render(request, "buscar_Cedula.html")

id_paciente_documentoID = None

def set_id_paciente_documentoID(id_paciente):
    global id_paciente_documentoID
    id_paciente_documentoID = id_paciente

def get_id_paciente_documentoID():
    global id_paciente_documentoID
    return id_paciente_documentoID

@method_decorator(csrf_exempt)
def BuscarCedula(request):
    cedulaPaciente = request.POST.get('cedula')
    try:
        paciente = Paciente.objects.filter(DocumentoId=cedulaPaciente).values_list('id',flat=True)[0]
        set_id_paciente_documentoID(paciente)
        return redirect('/agendar_cita')
    except Exception as e:
        messages.warning(request,'No se ha encontrado un paciente con este número de cédula')
        return render(request,"buscar_Cedula.html")