#Importes de Renders Y Responses
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

#Importes de Utilidades Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

#Importes de utilidades
import mysql.connector
from mysql.connector import errorcode
import datetime
import qrcode 
from reportlab.pdfgen.canvas import Canvas 
from reportlab.lib.utils import Image, ImageReader 
from reportlab.lib.pagesizes import letter

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

#Importes de métodos triviales
from Software2.Methods import EliminarSimbolos, CursorDB, GenerateUserByCorreoElement, send_email

#Importes de Modelos y Vistas
from GestionDeCitas.models import Cita, Paciente, Especialidad, Medico
from Autenticacion.views import get_nombreUsuario, set_nombreUsuario, get_is_logged_in, set_is_logged_in

@never_cache
@method_decorator(csrf_exempt)
def principal(request):
	print("Request principal: ",request.POST)
	print("Logout usuario: {} ---- is logged in: {}".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")
	request.session.flush() #Elimina la sesion actual --> django.session en la bd
	set_is_logged_in(None)
	set_nombreUsuario(None)
	print("|-- Sesion finalizada: {} | Sesion: {} --|".format(get_nombreUsuario(),get_is_logged_in()))
	print("\n")

	pdfGenerator()
	print('Pdf Generado')
	return render(request,"principalPage.html")

def pdfGenerator(id_paciente = 1):
	try:
		PacienteP = list(Paciente.objects.filter(id=id_paciente).values())
		CitaP = list(Cita.objects.filter(PacienteConCita_id=id_paciente).values())

		nombre_Paciente = "%s %s" %(PacienteP[0]["PrimerNombre"], PacienteP[0]["PrimerApellido"])
		documento_Paciente = "%s"%(PacienteP[0]["DocumentoId"])

		temp_medico_Cita = "%s"%(CitaP[0]["MedicoAsignado_id"])
		temp_especialidad_Cita = "%s"%(CitaP[0]["Especialidad_id"])
		
		MedicoP = list(Medico.objects.filter(id=temp_medico_Cita).values())
		EspecialidadP = list(Especialidad.objects.filter(id=temp_especialidad_Cita).values())

		medico_Cita = "%s %s"%(MedicoP[0]["PrimerNombre"], MedicoP[0]["PrimerApellido"])
		especialidad_Cita = "%s"%(EspecialidadP[0]["nombre"])
		fecha_Cita = "%s"%(CitaP[0]["DiaCita"])
		hora_Cita = "%s"%(CitaP[0]["HorarioCita"]) 

		canvass = Canvas("Cita.pdf", pagesize=letter)
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

def citas_del_dia(request):
	cita = Cita.objects.filter(DiaCita=timezone.now())
	print(cita)
	citas = []
	for a in cita:
		list_Cita = {'nombre':"%s %s" %(a.PacienteConCita.PrimerNombre, a.PacienteConCita.PrimerApellido),'hora': a.HorarioCita, 'motivo': a.MotivoConsultaCita}
		citas.append(list_Cita)

	return render(request, "./citas_del_dia.html",{"lista":citas})

def correo(request):
	if request.method == 'POST':
		mail = request.POST.get('mail')
		User = GenerateUserByCorreoElement(mail)
		send_email(mail, User[0], User[1], "./correo.html" )
		
	return render(request, "./regisCorreo.html")

lista = [1,2,3,4]
def histo_Paciente(request):
	
	return render(request, "./histo_Paciente.html", {"lista":lista})

#FORMA DE HACER CONSULTAS USANDO QUERY SETS DE SQL
cnx = mysql.connector.connect(user='root', password='Sistemas132',host='127.0.0.1',database='dbipsacme')
def vistaDoctor(request):
	
	cursor= CursorDB(cnx)

	#Consulta para buscar	 el nombreCompleto de los pacientes
	query = ("SELECT PrimerNombreP, SegundoNombreP, PrimerApellidoP, SegundoApellidoP FROM paciente")
	#(¿¿)Agregar WHERE cita.día = Today (??)

	consulta = cursor.execute(query)	
	pacientes =[]

	for i in cursor:
		P1= Paciente(EliminarSimbolos(i),"10:00 ")
		pacientes.append(P1)

	#Declara un objeto Doctor
	D1 =doctor("Miguel","Lizarazo")
	ahora = datetime.datetime.now()
	
	#Define un diccionario con lo que será necesario para mostrarse en el html
	diccionario = {"nombre_doctor":D1.nombre, "apellido_doctor":D1.apellido, "Hoy":ahora, "pacientes":pacientes}

	#Devuelve el html y el diccionario 
	return render(request, 'PlantillaDoctor.html', diccionario ) 