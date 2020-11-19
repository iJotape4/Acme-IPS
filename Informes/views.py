from django.shortcuts import render

from datetime import date, datetime, time, timedelta
from django.utils import timezone

from GestionDeCitas.models import Cita


def informe_Ips(request):
	lista = [1,2,3,4]
	return render(request, "./informe_IPS.html",{"lista":lista})

def informe_secretaria(request):
	citas= Cita.objects.filter(DiaCita=(datetime.now()+ timedelta(days=1)).date())
	lista=[]
	for a in citas:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita, 'numero' :a.PacienteConCita.Telefono}
		lista.append(list_Cita)
	return render(request, "informe_secretaria.html",{"lista":lista})