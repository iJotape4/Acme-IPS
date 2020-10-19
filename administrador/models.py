from django.db import models
from GestionDeCitas.models import Usuario

# Create your models here.
class Administrador(Usuario):  
	pass

class ReporteAdministrador(models.Model):
	FechaReporte = models.DateField()

	ModalidadCitaFrecuente= models.CharField(max_length=300)
	MedicosAusentes= models.CharField(max_length=300)

	PacientesDia= models.IntegerField()
	NumCitasCanceladas= models.IntegerField()  
	NumCitasConfirmadasAuto= models.IntegerField()  
	NumCitasConfirmadasManal= models.IntegerField()    

