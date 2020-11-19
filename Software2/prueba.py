from datetime import date, datetime, time, timedelta

def EliminarSimbolos(x):
	x = str(x).replace("'","").replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace(" ","")
	return x

def FormatFecha(date):

	fecha = date.split('/')
	
	invertir = [fecha[2], '/', fecha[1],'/', fecha[0]]

	formatear = datetime.strptime(EliminarSimbolos(str(invertir)),"%Y/%m/%d").date()

	return formatear			


def discard(horarios):	
	horarioExistente = time(13,0,0)
	for posibleHorario in horarios:
			if posibleHorario==horarioExistente or posibleHorario==time(12,0) or posibleHorario==time(0,0):
				print(posibleHorario)
				horarios.remove(posibleHorario)
	print(horarios)					   


def Generar(horarioLLegada, horarioSalida):
	horarios =[]

	horaLlega = horarioLLegada.strftime("%H")
	minLlega = horarioLLegada.strftime("%M")

	horaSale = horarioSalida.strftime("%H")

	horarioCita = horarioLLegada
	horaNueva= horaLlega
	minNuevo= minLlega

	while (time(int(horaNueva), int(minNuevo)) != horarioSalida)  and (int(horaNueva)+1<= int(horaSale)):
		if int(minNuevo)+30 <60:
			Oper = int(minNuevo)+30
			minNuevo = str(Oper)
			horarios.append(time(int(horaNueva), Oper) )
		else:
			res = (int(minNuevo)+30)-60
			hor = int(horaNueva)+1

			horaNueva = str(hor)
			minNuevo = str(res)

			horarios.append(time(hor, res))	
	discard(horarios)
	return horarios

def SumarDía(dia):
	dia = (dia + timedelta(days=1)).date()
	print(dia)

SumarDía(datetime.now())	