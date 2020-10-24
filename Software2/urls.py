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
from Software2.vistas.view import registro, vistaDoctor, principal, correo, histo_Paciente, menu_Paciente
from Software2.vistas.view import agendar_Cita, citas_del_dia, menu_admin, agregar_Medico, informe_Ips, recuperar_Contra
from Software2 import settings
from GestionDeCitas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registro/',registro),
    path('registrarse/', views.registrarse),
    path('login/',views.login),
    path('logearse/',views.logearse), 
   	path('Doctor/', vistaDoctor),
    path('principal/', principal ),
    path('correo/', correo ),
    path('his_paciente/', histo_Paciente ),
    path('menu_Paciente/', menu_Paciente ),
    path('agendar_cita/', agendar_Cita ),
    path('citas_del_dia/', citas_del_dia ),
    path('admin_menu/', menu_admin ),
    path('add_Medico/', agregar_Medico ),
    path('informe_IPS/', informe_Ips ),
    path('selectFecha/',views.selectFecha),
    path('recuperarContra/',recuperar_Contra),
]
