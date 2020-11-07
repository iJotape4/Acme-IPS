from django.shortcuts import render
from GestionDeCitas.models import Cita
from django.utils import timezone
# Create your views here.
lista = [1,2,3,4]

def informe_Ips(request):
	return render(request, "./informe_IPS.html",{"lista":lista})

def citas_del_dia(request):
	cita = Cita.objects.filter(DiaCita=timezone.now())
	print(cita)
	citas = []
	for a in cita:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita}
		citas.append(list_Cita)

	return render(request, "./citas_del_dia.html",{"lista":citas})