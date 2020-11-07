"""Software2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Software2.views import vistaDoctor, principal, correo, histo_Paciente, citas_del_dia, menu_secretaria, informe_secretaria
from Software2 import settings
from administrador.views import menu_admin, agregar_Medico
from GestionDeCitas.views import AgendarCitaView, AgendarCita
from Informes.views import informe_Ips
from Autenticacion.views import login, recuperar_Contra, registrarse, registro, menu_Paciente

urlpatterns = [
    # Administrador
    path('admin/', admin.site.urls),
    path('administrador_menu/', menu_admin ),
    path('menu_secre/', menu_secretaria),
    path('informeSecre/', informe_secretaria ),
    # Registro
    path('registro/',registro, name='registro'),
    path('registrarse/', registrarse),
    # Login
    path('login/', login, name='login'),
    path('recuperarContraseña/', recuperar_Contra),
    # Doctor
   	path('menu_Doctor/', vistaDoctor),
    # Pagina principal
    path('principal/', principal, name='principal'),
    path('correo/', correo, name='correo'),
    # Paciente
    path('historial_paciente/', histo_Paciente ),
    path('menu_Paciente/', menu_Paciente, name='memu_paciente'),
    # Agendar Cita
    path('agendar_cita/', AgendarCitaView.as_view(template_name="agendamiento_Citas.html"), name= 'agendar'),
    path('citas_del_dia/', citas_del_dia, name='citasDía'),
    # 
    path('agregar_Medico/', agregar_Medico ),
    path('informe_IPS/', informe_Ips ),
    path('guardarCita/', AgendarCita)
]
