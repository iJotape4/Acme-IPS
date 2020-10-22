from django.shortcuts import render
from django.http import HttpResponse
from GestionDeCitas.models import Paciente
from django.contrib.auth import logout as do_logout
from django.shortcuts import render, redirect
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional

def login(request):
    return render(request, "./login.html")

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

        #Esto condiciona a que ambos existan y coincidan (creo)
        if user:       
            return render(request, "menu_Paciente.html", {"userlogeado":nombre})
        else:
            return HttpResponse("Paciente No existe")
        
    else:
        mensaje="Al menos uno de los campos está vacío"
    return HttpResponse(mensaje)

def registro(request):
    return render(request, "./registro.html")

def comprobar_DatoNumerico(lista):
    for dato in range(len(lista)):
        if dato == 4 or dato == 6 or dato == 8 or dato == 9:
            if lista[dato].isnumeric()==False:
                return False
    return True

def verificar_Existencia_Usuarios(documentoId):
    user = Paciente.objects.filter(DocumentoId=documentoId)
    return len(user)

def registrarse(request):
    #### IMPORTANTE ####
    # Usuario y contraseña deben ser tomados desde el correo enviado. 
    # La vista de login se abre desde un hipervículo en el correo enviado
    datos_Registro = [data for data in (request.GET).values()]
    datos_Registro_Check = [
        datos_Registro[data] for data in range(len(datos_Registro)) 
        if data!=12 and data!=16
    ]
    
    print(datos_Registro)
    print(datos_Registro_Check)
    if len(datos_Registro_Check)==16:
           #Validacion de que los campos edad, documento, telefono y whatsapp sean numericos
           #Validacion de que todos los campos esten llenos
        if comprobar_DatoNumerico(datos_Registro):
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
            else:
                return HttpResponse("Ya existe un usuario con esté número de cédula")
        else:
            return HttpResponse("Los campos de edad, telefono, WhatsApp y documento de identidad deben ser numericos")
    else:
        return HttpResponse("Por favor, rellena todos los campos")
    return render(request,"./login.html")
   