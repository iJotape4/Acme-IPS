from django.db import models
import mysql.connector
from mysql.connector import errorcode
import pymysql

# Create your models here.
class Usuario(models.Model):
	class Meta:
		abstract=True

	PrimerNombre = models.CharField(max_length=50)
	SegundoNombre = models.CharField(max_length=50)
	PrimerApellido = models.CharField(max_length=50)
	SegundoApellido = models.CharField(max_length=50)
	Usuario = models.CharField(max_length=50)
	Contraseña= models.CharField(max_length=50)
	DocumentoId= models.IntegerField()
	TipoDocumento= models.CharField(max_length=50)
	Edad = models.IntegerField()
	CorreoElectronico = models.CharField(max_length=90)
	TipoUsuario = models.CharField(max_length=20, default='Usuario')

class ciudad(models.Model):
    NombreC = models.CharField(max_length=70)
    DepartamentoC = models.CharField(max_length=70)

class Paciente(Usuario):  
	EPSP = models.CharField(max_length=90)
	Telefono = models.CharField(max_length=20)
	Whatsapp = models.CharField(max_length=20)

class Medico(Usuario):  
	HorarioLlegada = models.DateField()
	HoraioSalida = models.DateField()

class Secretaria(Usuario):  
	Whatsapp = models.CharField(max_length=20)

class ReporteSecretaria(models.Model):  
	FechaReporte = models.DateField()

class Cita(models.Model):
	ModalidadCita = models.CharField(max_length=10)
	MotivoConsultaCita = models.CharField(max_length=15)
	EspecialidadCita = models.CharField(max_length=50)
	HorarioCita = models.DateField()
	CitaPagada = models.BooleanField(default=0)
	Asistencia = models.BooleanField(default=0)
	MedicoAsignado = models.ForeignKey(Medico, on_delete=models.CASCADE)
	PacienteConCita = models.ForeignKey(Paciente, on_delete=models.CASCADE)
	ReporteSec = models.ForeignKey(ReporteSecretaria, on_delete=models.CASCADE)

class Acudiente(models.Model):  
	NombreAcu = models.CharField(max_length=50)
	TelefonoAcu = models.CharField(max_length=11)
	ParentescoAcu = models.CharField(max_length=20)
	Apadrinado = models.ForeignKey(Paciente, on_delete=models.CASCADE)



class ClassName(object):
	"""docstring for ClassName"""
	def __init__(self, arg):
		super(ClassName, self).__init__()
		self.arg = arg
		