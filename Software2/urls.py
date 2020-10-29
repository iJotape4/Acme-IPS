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
from Software2.views import vistaDoctor, principal, correo, histo_Paciente, menu_Paciente, citas_del_dia
from Software2 import settings
from administrador.views import menu_admin, agregar_Medico
from GestionDeCitas.views import selectFecha, AgendarCitaView
from Informes.views import informe_Ips
from Autenticacion.views import logearse, login, recuperar_Contra, registrarse, registro

urlpatterns = [
    # Administrador
    path('admin/', admin.site.urls),
    path('admin_menu/', menu_admin ),
    # Registro
    path('registro/',registro),
    path('registrarse/', registrarse),
    # Login
    path('login/', login),
    path('logearse/', logearse), 
    path('recuperarContra/', recuperar_Contra),
    # Doctor
   	path('Doctor/', vistaDoctor),
    # Pagina principal
    path('principal/', principal ),
    path('correo/', correo ),
    # Paciente
    path('his_paciente/', histo_Paciente ),
    path('menu_Paciente/', menu_Paciente ),
    # Agendar Cita
    path('agendar_cita/', AgendarCitaView.as_view(template_name="agendamiento_Citas.html")),
    path('citas_del_dia/', citas_del_dia ),
    # 
    path('add_Medico/', agregar_Medico ),
    path('informe_IPS/', informe_Ips ),
    path('selectFecha/', selectFecha),
]
