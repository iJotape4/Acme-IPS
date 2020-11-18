#Importes de Renders Y Responses
from django.shortcuts import render, redirect
from django.http import JsonResponse

#Importes de utilidades
from django import forms
from django.contrib import messages
from django.utils import timezone
from datetime import date, datetime

#Importes de decoradores
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

#Importes de métodos Triviales
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional, EliminarSimbolos 
from Software2.Methods import send_email, GenerarHorarioCitas
from Software2.Methods import  get_tipoUsuario, set_tipoUsuario, ReturnHtmlMenuUsuario, citas_del_dia


#Importes de Modelos y Vistas
from GestionDeCitas.models import Paciente, Medico, Secretaria, Cita
from administrador.models import Administrador



class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

nombre_Usuario = None
id_Usuario = None
is_logged_in = False
tipoUsuario = None

def set_nombreUsuario(nombre):
    global nombre_Usuario
    nombre_Usuario = nombre

def get_nombreUsuario():
    global nombre_Usuario
    return nombre_Usuario

def set_idUsuario(id):
    global id_Usuario
    id_Usuario = id    

def get_idUsuario():
    global id_Usuario
    return id_Usuario    

def set_is_logged_in(response):
    global is_logged_in
    is_logged_in = response

def get_is_logged_in():
    global is_logged_in
    return is_logged_in



username = None
password = None
def set_username(nombre):
    global username
    username = nombre

def get_username():
    global username
    return username

def set_password(id):
    global password
    password = id    

def get_password():
    global password
    return password

@never_cache
def login(request):
    return render(request,'login.html')

@never_cache
@method_decorator(csrf_exempt)
def menu_Paciente(request):
    #El if comprueba si los campos están llenos
    if request.POST.get("username") and request.POST.get("password"):
        #Esto recupera los datos en los campos
        usuario = request.POST.get("username")
        contra = request.POST.get("password")
            
        set_nombreUsuario(logearse(usuario,contra,'nombre'))
        set_idUsuario(logearse(usuario,contra,'id'))
        set_tipoUsuario(logearse(usuario,contra,'tipoUsuario'))

        if get_nombreUsuario() != None:
            request.session['usuario'] = usuario #Se crea una session en la bd con la sesion actual
            set_is_logged_in(True)
            print("\n")
            print("sesion parseada: ",request.session['usuario'])
            print("Nombre de usuario: ",get_nombreUsuario())
            print(request.body)
            print("\n")        
            if(get_tipoUsuario()=="Medico"):
                return render(request,"./citas_del_dia.html", {'lista':citas_del_dia(get_idUsuario()),"userlogeado":get_nombreUsuario(),'logeado':request.session['usuario']})               
            else:
                return render(request,ReturnHtmlMenuUsuario(),{"userlogeado":get_nombreUsuario(),'logeado':request.session['usuario']})
        else:
            messages.warning(request,'Ups, parece que no existe un usuario con estas credenciales')
            return login(request)
    else:
        set_nombreUsuario(None)
        set_is_logged_in(None)
        set_idUsuario(None)
        return login(request)


def logearse(usuario,contra,atributo_a_buscar):
    #Esto busca en la base de datos ese usuario y contraseña
    user = Paciente.objects.filter(Usuario=usuario, Contraseña=contra)
    if len(user)==0:
        user= Secretaria.objects.filter(Usuario=usuario, Contraseña=contra)
    if len(user)==0:
        user= Medico.objects.filter(Usuario=usuario, Contraseña=contra)
    if len(user)==0:
        user= Administrador.objects.filter(Usuario=usuario, Contraseña=contra)        

    if atributo_a_buscar=='nombre':
        for e in user:
            nombre = "%s %s" %(e.PrimerNombre, e.PrimerApellido)            
        #Esto condiciona a que ambos existan y coincidan
        if user:   
            print("nombre: ",nombre)        
            return nombre
        #Para cuando lo que se quiere obtener es el id    
    elif atributo_a_buscar == 'id':
        for e in user:
            id = e.DocumentoId 
            print("doc"+str(id))
        if user:
            return id
    elif atributo_a_buscar == 'tipoUsuario':
        for e in user:
            tipo = e.TipoUsuario 
            print("tipo"+str(tipo))
        if user:
            return tipo           
    return None
    
def registro(request,username="default",password="default"):
    print(username)
    print(password)
    if username!="default" and password!="default":
        set_username(username)
        set_password(password)
    return render(request,"registro.html")

def recuperar_Contra(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        paciente = Paciente.objects.filter(CorreoElectronico=email)
        if paciente:
            send_email(email, paciente[0].Usuario, paciente[0].Contraseña, "./correoRecuperar.html")
            return render(request,"recuperarContra.html")
        else:
            messages.warning(request, "No existe un usuario Registrado con ese correo electrónico") 
            return render(request, "recuperarContra.html")   
		##Falta redireccionar bien
    return render(request, "recuperarContra.html")       

def registrarse(request):
    #### IMPORTANTE ####
    # Usuario y contraseña deben ser tomados desde el correo enviado. 
    # La vista de login se abre desde un hipervículo en el correo enviado
    datos_Registro = [data for data in (request.GET).values()]
    datos_Registro_Check = [
        datos_Registro[data] for data in range(len(datos_Registro)) 
        if data!=12 and data!=16
    ]

    #Esto recupera los datos en los campos       
    primerNombre = request.GET["pri_Nombre"] 
    segundoNombre = request.GET["seg_Nombre"] 
    primerApellido = request.GET["pri_Apellido"] 
    segundoApellido = request.GET["seg_Apellido"] 
    documentoId= request.GET['Documento_Id'] 
    tipoDocumento= request.GET["tipo_documento"] 
    edad = request.GET["edad"] 
    correoElectronico = request.GET["email"] 

    eps = request.GET["eps"]
    telefono = request.GET["telefono"]
    whatsapp = request.GET["whatsapp"]

    otros = request.GET["otros"]
    ciudad = request.GET["ciudad"]
    barrio = request.GET["barrio"]
    complemento = request.GET["complemento"]

    hipertension = DefinirCondiciónMedica(str(request.GET["hipertension"]))
    diabetes = DefinirCondiciónMedica(str(request.GET["diabetes"]))
    cardiacos = DefinirCondiciónMedica(str(request.GET["cardiacos"]))
    
    Paciente.objects.create(PrimerNombre=primerNombre, SegundoNombre=segundoNombre, 
    PrimerApellido=primerApellido, SegundoApellido=segundoApellido, DocumentoId=documentoId,
    Edad=edad, CorreoElectronico=correoElectronico, TipoUsuario='Paciente', EPSP=eps, Telefono=telefono, Whatsapp=whatsapp,
    TipoDocumento=tipoDocumento, Otros=otros,Ciudad=ciudad, Barrio=barrio, complemento=complemento, 
    Hipertension=hipertension, Diabetes=diabetes, Cardiacos=cardiacos, Usuario=get_username(),Contraseña=get_password(),)
    return redirect("/login")