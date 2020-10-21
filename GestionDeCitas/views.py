from django.shortcuts import render
from django.http import HttpResponse
from GestionDeCitas.models import Paciente
from Software2.Methods import DefinirCondiciónMedica

# Create your views here.
def login(request): 
    return render(request,"./login.html")

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

    #Esto condiciona a que exista
        if user:       
            Paciente.objects.create(PrimerNombre="primerNombre", SegundoNombre="segundoNombre")
            return render(request, "menu_Paciente.html", {"userlogeado":nombre})
        else:
            return HttpResponse("Paciente No existe")
        
    else:
        mensaje="Al menos uno de los campos está vacío"
    return HttpResponse(mensaje)

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

    return render(request,"./login.html")
   