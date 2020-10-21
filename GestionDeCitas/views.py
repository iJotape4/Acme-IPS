from django.shortcuts import render
from django.http import HttpResponse
from GestionDeCitas.models import Paciente
from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional

def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/login.html')

    # Si llegamos al final renderizamos el formulario
    return render(request, "./login.html", {'form': form})


def logearse(request):
    #El if comprueba si los campos están llenos
    if request.GET["username"] and request.GET["password"]:

    #Esto recupera los datos en los campos
        usuario = request.GET["username"]
        contra = request.GET["password"] 

    #Esto busca en la base de datos ese usuario y contraseña
        user = Paciente.objects.filter(Usuario=usuario) and Paciente.objects.filter(Contraseña=contra)
        for e in user:
            nombre= "%s %s" %(e.PrimerNombre, e.PrimerApellido)            
        
        #Paciente.objects.create(PrimerNombre="alv",SegundoNombre="dsa",PrimerApellido="wqe",SegundoApellido="jjj",Usuario="melvin",Contraseña="000",DocumentoId="495992394",TipoDocumento="CC",Edad="50",CorreoElectronico="eurhf.unab.edu.co",EPSP="Nueva EPS",Telefono="5234234",Whatsapp="9130239012",TipoUsuario="MasteChief")
        print("PRUEBA ---> ",type(request))
    #Esto condiciona a que ambos existan y coincidan (creo)
        if user:       
            return render(request, "menu_Paciente.html", {"userlogeado":nombre})
        else:
            return HttpResponse("Paciente No existe")
        
    else:
        mensaje="Al menos uno de los campos está vacío"
    return HttpResponse(mensaje)

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/principal')


def registro(request):

    return render(request, "./registro.html")

def registrarse(request):
    #### IMPORTANTE ####
    # Usuario y contraseña deben ser tomados desde el correo enviado. 
    # La vista de login se abre desde un hipervículo en el correo enviado
    

    #Falta validar que los campos no estén vacíos
    #if request.GET["pri_Nombre"] and request.GET["seg_Nombre"]:

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
    
    otros = CampoOpcional(request, "otros")
    
    ciudad = request.GET["ciudad"]
    barrio = request.GET["barrio"]

    complemento = CampoOpcional(request, "complemento")

    hipertension = DefinirCondiciónMedica(str(request.GET["hipertension"]))
    diabetes = DefinirCondiciónMedica(str(request.GET["diabetes"]))
    cardiacos = DefinirCondiciónMedica(str(request.GET["cardiacos"]))
  
    Paciente.objects.create(PrimerNombre=primerNombre, SegundoNombre=segundoNombre, 
    PrimerApellido=primerApellido, SegundoApellido=segundoApellido, DocumentoId=documentoId,
    Edad=edad, CorreoElectronico=correoElectronico, TipoUsuario='Paciente', EPSP=eps, Telefono=telefono, Whatsapp=whatsapp,
    TipoDocumento=tipoDocumento, Otros=otros,Ciudad=ciudad, Barrio=barrio, complemento=complemento, 
    Hipertension=hipertension, Diabetes=diabetes, Cardiacos=cardiacos)

    return render(request,"./login.html")
   