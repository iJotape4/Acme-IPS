import mysql.connector
from mysql.connector import errorcode
import random

from datetime import datetime

def EliminarSimbolos(x):
	x = str(x).replace("'","").replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace(" ","")
	return x

def CursorDB(cnx):
	Cursor = cnx.cursor()
	return Cursor

def DefinirCondiciónMedica(condicion):
	if condicion=='si':
		return True
	else:
		return False

def GenerateUserByCorreoElement(email):
	userArray=[]
	passwordArray=[]
	for e in email:
		if e == '@' or e=='.' :
			pass
		else:
			if email.index(e) % 2 ==0:
				passwordArray.append(e)
			else:
				userArray.append(e)
	random.shuffle(userArray)
	random.shuffle(passwordArray)
	
	User = [EliminarSimbolos(userArray),EliminarSimbolos(passwordArray)] 
	return User

def CampoOpcional(request, campo):
	if request.GET[campo]:
		variable = request.GET[campo]
	else:
		variable = ''
	return variable	


def GenerarHorarioCitas(horarioLLegada, horarioSalida):
	horarios =[horarioLLegada]

	horaLlega = horarioLLegada.strftime("%H")
	minLlega = horarioLLegada.strftime("%M")

	horaSale = horarioSalida.strftime("%H")

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

#def GenerarHorarioCitas(horarioSalida, horarioLLegada):




