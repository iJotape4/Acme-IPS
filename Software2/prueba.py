import random
from datetime import datetime

def GenerarHorarioCitas(horarioLLegada, horarioSalida):
	horarios =[horarioLLegada]

	horaLlega = horarioLLegada.strftime("%H")
	minLlega = horarioLLegada.strftime("%M")

	horaSale = horarioSalida.strftime("%H")

	horarioCita = horarioLLegada
	horaNueva= horaLlega
	minNuevo= minLlega

	while (datetime.strptime(horaNueva+":"+minNuevo,"%H:%M") <= horarioSalida)  and (int(horaNueva)+1<= int(horaSale)):
		if int(minNuevo)+30 <60:
			Oper = int(minNuevo)+30
			minNuevo = str(Oper)
			horarios.append(datetime.strptime(horaNueva+":"+str(Oper), "%H:%M") )  
		else:
			res = (int(minNuevo)+30)-60
			hor = int(horaNueva)+1

			horaNueva = str(hor)
			minNuevo = str(res)

			horarios.append(datetime.strptime(str(hor)+":"+str(res), "%H:%M" ))	

	return horarios


print(GenerarHorarioCitas(datetime.strptime("13:50","%H:%M"), datetime.strptime("23:50","%H:%M" )))