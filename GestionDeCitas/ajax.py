from django.http import JsonResponse
from django.shortcuts import render, redirect

from GestionDeCitas.models import Paciente,Medico,Horario,Especialidad,Cita
from Software2.Methods import GenerarHorarioCitas

def get_medicos(request):
    especialidadesdb = Especialidad.objects.all()
    print("\n",especialidadesdb)
    especialidades = list()
    for a in especialidades:
        #list_Especialidades = {'especialidad':"%s"(a.Especialidad.nombre)}
        #especialidades.append(list_Especialidades)
        pass
    print("\n",especialidades)
    return render(request,'agendar_citaP.html',{'list':especialidades})
       
def get_horarios(request):
    medico = request.GET["medico"] 
    horarios =  Horario.objects.none()
    options = '<option value="" selected="selected">--- ------</option>'

    if medico:
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
    
    #horarioLlegada = medicoBD[0].HorarioLlegada
    #horarioSalida = medicoBD[0].HorarioSalida

    horarios = GenerarHorarioCitas(medicoBD[0].horario.horarioLLegada, medicoBD[0].horario.horarioSalida)

    for horario in horarios:
        options+='<option value="%s">%s</option>' % (
            horario,horario)
    
    response = {}
    response['horarios'] =options
    return JsonResponse(response)
      