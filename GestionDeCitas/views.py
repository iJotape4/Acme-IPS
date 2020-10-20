from django.shortcuts import render
from django.http import HttpResponse
from GestionDeCitas.models import Paciente

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
        user = Paciente.objects.filter(Usuario=usuario)
        password = Paciente.objects.filter(Contraseña=contra)

    #Esto condiciona a que ambos existan y coincidan (creo)
        if user and password:       
            return render(request, "menu_Paciente.html", {"userlog":user, "query":usuario})
        else:
            return HttpResponse("Paciente No existe")
        
    else:
        mensaje="Al menos uno de los campos está vacío"
    return HttpResponse(mensaje)