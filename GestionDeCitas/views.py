from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from Software2.Methods import send_email, GenerarHorarioCitas
from django.contrib import messages
from django import forms
from GestionDeCitas.models import Paciente, Medico,Horario,Especialidad,Cita
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from GestionDeCitas.forms import AgendarCitaForm
from Autenticacion.views import login

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
       
        print("\n Filtrar Medicos")
        print(respuesta)
        print("\n")
        especialidad = respuesta[1]
        AgendarCitaView.especialidad_AJAX = especialidad

        especialidad_AJAX = especialidad
        id_especialidad_Escogida = list(Especialidad.objects.filter(nombre=especialidad).values_list('id',flat=True))
        
        filtro = list(Medico.objects.filter(especialidad_id=id_especialidad_Escogida[0]).values())
        for dato in filtro:
            data.append({'PrimerNombre': dato['PrimerNombre'],'PrimerApellido':dato['PrimerApellido']})
        return data

    def filtrar_Horarios(self,data,respuesta):
        print("\n Filtrar horarios")
        print(respuesta)
        print("\n")
        medico = respuesta[1]
        AgendarCitaView.medico_AJAX = medico

        id_Horario_Escogido = list(Medico.objects.filter(PrimerNombre=medico).values_list('horario_id',flat=True))
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

def selectFecha(request): #GestionCitas
    print("--------------------")
    print(request.GET.get('fecha'))
    print("--------------------")
    return login(request)

@method_decorator(csrf_exempt)
def AgendarCita(request):
    form = AgendarCitaForm()
        
    if request.method == 'POST':
        form = AgendarCitaForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/menu_Paciente/')
        return render(request, 'AgendarCita_Prueba.html', {'form':form})       

    tipoCita = request.GET["tipoCita"] 
    especialidad = request.GET["especialidad"] 
    nmedicos = []
    medicos = Medico.objects.filter(Especialidad=especialidad)
    
    for e in medicos:
        nombre= "%s %s %s %s" %(e.PrimerNombre, e.SegundoNombre, e.PrimerApellido, e.SegundoApellido)
        nmedicos.append(nombre) 

    medico = request.GET["medico"]

    medicoElegido =[]
    temporal=[]
    for e in medico:
        if(e==' '):
            medicoElegido.append(temporal)
            temporal=[]
        else:
            temporal.append(e)
    #EliminarSimbolos(str(medicoElegido))

    medicoBD = Medico.objects.filter (
        PrimerNombre=medicoElegido[0],
        SegundoNombre=medicoElegido[1],
        PrimerApellido=medicoElegido[2],
        SegundoApellido=medicoElegido[3]
        )

    horarioLlegada = medicoBD[0].HorarioLlegada
    horarioSalida = medicoBD[0].HorarioSalida 

    horarios = horarioLlegada

    #horario = request.GET["Horario"]
    #motivoConsulta = request.GET["MotivoDeConsulta"]  
    diccionario ={"medicos":nmedicos, "horarios":horarios}

    return render(request,"principal_Paciente.html",diccionario)
