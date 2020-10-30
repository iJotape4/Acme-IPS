
#Importes de utilidades DJango
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

#Importes de Archivos del proyecto
from GestionDeCitas.models import Paciente
from Software2 import settings

#Importes de funciones
import random
from datetime import datetime, time

#importes de Modelos
from GestionDeCitas.models import Medico, Cita

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


def GenerarHorarioCitas(horarioLLegada, horarioSalida, medicoElegido):
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
	DiscardAlreadyAssignedSchedules(horarios, medicoElegido)
	return horarios

def DiscardAlreadyAssignedSchedules(horarios, medicoElegido):
	MedicoC =Medico.objects.filter(PrimerNombre=medicoElegido[0], PrimerApellido=medicoElegido[1])[0]
	horarios_existentes = list(Cita.objects.filter(MedicoAsignado=MedicoC).values_list('HorarioCita',flat=True))

	for  horarioExistente in horarios_existentes:
		for posibleHorario in horarios:
			if posibleHorario==horarioExistente:
				horarios.remove(posibleHorario)
	return horarios			   

def DiscardMedicsWhit12Citas(filtro, fecha):
	medicos = []
	for dato in filtro:
		Citas=  list(Cita.objects.filter(MedicoAsignado_id=dato['id'], DiaCita=fecha).values_list('id',flat=True))
		if len(Citas)<12:
			medicos.append(dato)
	return medicos		


                  

def send_email(mail, usuario, password, CorreoHTML):
	context = {'mail': mail, 'user':usuario, 'password':password}

	template = get_template(CorreoHTML)
	content = template.render(context)

	email = EmailMultiAlternatives(
		'Usuario IPS ACME',
		'Estos son su usuario y contraseña. ',
		settings.EMAIL_HOST_USER,
		[mail]
	)
	
	email.attach_alternative(content, 'text/html')
	email.send()   

def verificar_Existencia_Usuarios(documentoId):
    user = Paciente.objects.filter(DocumentoId=documentoId)
    return len(user)

def comprobar_DatoNumerico(lista):
    for dato in range(len(lista)):
        if dato == 4 or dato == 6 or dato == 8 or dato == 9:
            if lista[dato].isnumeric()==False:
                return False
    return True

def FormatFecha(date):

	fecha = date.split('/')
	
	invertir = [fecha[2], '/', fecha[1],'/', fecha[0]]

	formatear = datetime.strptime(EliminarSimbolos(str(invertir)),"%Y/%m/%d").date()

	return formatear	