
#Importes de utilidades DJango
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

#Importes de Archivos del proyecto
from GestionDeCitas.models import Paciente
from Software2 import settings

#Importes de funciones
import random
from datetime import datetime, time
import qrcode 

#Importes de utilidades
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import Image, ImageReader 
from reportlab.lib.pagesizes import letter

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


def GenerarHorarioCitas(horarioLLegada, horarioSalida, medicoElegido,fecha):
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
	DiscardAlreadyAssignedSchedules(horarios, medicoElegido,fecha)
	return horarios

def DiscardAlreadyAssignedSchedules(horarios, medicoElegido,fecha):
	MedicoC =Medico.objects.filter(PrimerNombre=medicoElegido[0], PrimerApellido=medicoElegido[1])[0]
	horarios_existentes = list(Cita.objects.filter(MedicoAsignado=MedicoC, DiaCita=fecha).values_list('HorarioCita',flat=True))

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

def qr_Code_Generator(documentoPaciente):
	try:
		qr = qrcode.QRCode(version=1,box_size=6,border=5)
		qr.add_data(documentoPaciente)
		qr.make(fit=True)
		img = (qr.make_image(fill='black', back_color='white')).get_image()
		img = ImageReader(img)
		return img
	except Exception as e:
		print("Ha ocurrido un error durante la generación del QR -> {}".format(e))


def pdfGenerator(citaCreada):
	try:		
		nombre_Paciente = "%s %s" %(citaCreada.PacienteConCita.PrimerNombre, citaCreada.PacienteConCita.PrimerApellido)
		documento_Paciente = "%s"%(citaCreada.PacienteConCita.DocumentoId)

		medico_Cita = "%s %s"%(citaCreada.MedicoAsignado.PrimerNombre,  citaCreada.MedicoAsignado.PrimerApellido)
		especialidad_Cita = "%s"%( citaCreada.Especialidad.nombre)
		fecha_Cita = "%s"%(citaCreada.DiaCita)
		hora_Cita = "%s"%(citaCreada.HorarioCita) 

		canvass = Canvas("%s C%s%s_%s"%(nombre_Paciente,citaCreada.id,especialidad_Cita[0],fecha_Cita), pagesize=letter)
		canvass.setLineWidth(.3)
		canvass.setFont('Helvetica', 12)
		canvass.drawString(80,725,'Nombre: '+str(nombre_Paciente))
		canvass.drawString(80,700,'Documento: '+ str(documento_Paciente))
		canvass.drawString(80,675,'Medico: '+ str(medico_Cita))
		canvass.drawString(80,650,'Especialidad: '+ str(especialidad_Cita))
		canvass.drawString(80,625,'Fecha Cita:'+ str(fecha_Cita))
		canvass.drawString(80,600,'Hora Cita: '+ str(hora_Cita))

		canvass.drawImage(qr_Code_Generator(str(documento_Paciente)),80,400)
		
		canvass.showPage()
		canvass.save()
        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        #buffer.seek(0)
        #return FileResponse(as_attachment=True, filename='hello.pdf')
	except Exception as e:
		print("Ha ocurrido un error durante la generación del PDF -> {}".format(e))
