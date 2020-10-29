from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.http import JsonResponse
from GestionDeCitas.models import Paciente
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from Software2.Methods import verificar_Existencia_Usuarios,comprobar_DatoNumerico
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional, EliminarSimbolos 
from Software2.Methods import send_email, GenerarHorarioCitas

#nombre_Usuario = ""
#is_logged_in = False
nombre = None #El nombre del usuario logueado - esta variable se pone en None tan pronto cierre sesion -> view.py

def login(request):
    return render(request,'login.html')

class DateForm(forms.Form):
    date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

def render_Menu_Paciente(request,contexto):
    print("sesion: ",request.session.keys())
    print("sesion parseada: ",request.session['usuario'])
    print("Nombre de usuario: ",nombre)
    print("\n")
    if 'usuario' in request.session and nombre!=None:
        return render(request,"menu_Paciente.html",contexto)
    else:
        print("\nEl usuario no se encuentra logueado para continuar\n")
        return render(request,"principalPage.html")

@method_decorator(csrf_exempt)
def logearse(request):
    global nombre
    
    #global nombre_Usuario
    #global is_logged_in 
    #El if comprueba si los campos están llenos
    if request.POST.get("username") and request.POST.get("password"):
        #Esto recupera los datos en los campos
        usuario = request.POST.get("username")
        contra = request.POST.get("password")

        #Esto busca en la base de datos ese usuario y contraseña
        user = Paciente.objects.filter(Usuario=usuario, Contraseña=contra)
        for e in user:
            nombre = "%s %s" %(e.PrimerNombre, e.PrimerApellido)            

        #Esto condiciona a que ambos existan y coincidan
        if user:   
            #nombre_Usuario = nombre
            #is_logged_in = True 
            request.session['usuario'] = usuario #Se crea una session en la bd con la sesion actual
            return render_Menu_Paciente(request,{"userlogeado":nombre,'logeado':request.session['usuario']})
        else:
            messages.warning(request,'Ups, parece que no existe un usuario con estas credenciales')
            return login(request)
    return login(request)  
    
def registro(request):
    return render(request,"registro.html")

def recuperar_Contra(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        paciente = Paciente.objects.filter(CorreoElectronico=email)
        if paciente:
            send_email(email, paciente[0].Usuario, paciente[0].Contraseña, "./correoRecuperar.html")
            return render(request, "recuperarContra.html")
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

    if verificar_Existencia_Usuarios(datos_Registro[6])==0:
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
        Hipertension=hipertension, Diabetes=diabetes, Cardiacos=cardiacos)

        return redirect("/login")
    else:
        return redirect("/registro")
