from django.contrib import admin
from django.urls import path
from Software2.views import principal, correo, menu_secretaria
from Software2 import settings

from administrador.views import menu_admin, AgregarMedicoView, AgregarMedico

from GestionDeCitas.views import AgendarCitaView, AgendarCita, reagendarPaciente, reagendarSecretaria 
from GestionDeCitas.views import histo_Paciente, buscarPacienteCC, BuscarCedula
from Informes.views import informe_Ips, informe_secretaria
from Autenticacion.views import login, recuperar_Contra, registrarse, registro, menu_Paciente

urlpatterns = [
    path('admin/', admin.site.urls),
    path('administrador_menu/', menu_admin ),
    path('menu_secre/', menu_secretaria),
    path('informeSecre/', informe_secretaria),
    path('registro/',registro, name="registroCorreo_Paciente"),
    path('registro/<username>/<password>/',registro, name='registro'),
    path('registrarse/', registrarse),
    path('login/', login, name='login'),
    path('recuperarContraseña/', recuperar_Contra, name='recuperar_Contra'),
    path('', principal, name='principal'),
    path('correo/', correo, name='correo'),
    path('historial_paciente/', histo_Paciente ),
    path('menu_Paciente/', menu_Paciente, name='memu_paciente'),
    path('agendar_cita/', AgendarCitaView.as_view(template_name="agendamiento_Citas.html"), name= 'agendar'),  
    path('agregar_Medico/', AgregarMedicoView.as_view(template_name="registrar_Medico.html"), name= 'agregar') ,
    path('AgregarMedico/', AgregarMedico),
    path('informe_IPS/', informe_Ips),
    path('AgendarCita/', AgendarCita),
    path('reagendarSecre/', reagendarSecretaria),
    path('reagendarPaci/', reagendarPaciente),
    path('buscarCC/', buscarPacienteCC),
    path('BuscarCedula/',BuscarCedula)
]
