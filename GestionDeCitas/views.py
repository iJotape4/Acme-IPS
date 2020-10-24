from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.core.urlresolvers  import reverse
from GestionDeCitas.models import Paciente, Medico,Horario,Especialidad,Cita
from GestionDeCitas.forms import AgendarCitaForm
from django.shortcuts import render, redirect
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional, EliminarSimbolos, send_email
from django.contrib import messages
from django import forms
from GestionDeCitas.models import Paciente,Medico,Horario,Especialidad,Cita
from django.http import JsonResponse
from Software2.Methods import GenerarHorarioCitas

nombre_Usuario = ""
is_logged_in = False

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

def render_Menu_Paciente(request,is_loggedIn,contexto):
    if is_loggedIn:
        return render(request,"menu_Paciente.html",contexto)
    else:
        print("\nEl usuario no se encuentra logueado para continuar\n")
        return render(request,"principal_Paciente.html")

def selectFecha(request):
    print("--------------------")
    print(request.GET.get('fecha'))
    print("--------------------")
    return login(request) 

def logearse(request):
    global nombre_Usuario
    global is_logged_in 
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
            nombre_Usuario = nombre
            is_logged_in = True 
            messages.success(request,'Has iniciado sesión con exito!!') 
            return render_Menu_Paciente(request,is_logged_in,{"userlogeado":nombre})
        else:
            messages.warning(request,'Ups, parece que no existe un usuario con estas credenciales')
            return login(request) 
    
def registro(request):
    return render(request,"registro.html")

def comprobar_DatoNumerico(lista):
    for dato in range(len(lista)):
        if dato == 4 or dato == 6 or dato == 8 or dato == 9:
            if lista[dato].isnumeric()==False:
                return False
    return True

def recuperar_Contra(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        paciente = Paciente.objects.filter(CorreoElectronico=email)
        if paciente:
            send_email(email, paciente[0].Usuario, paciente[0].Contraseña, "./correoRecuperar.html")
            return render(request, "recuperarContra.html")
        else:
            return messages("No existe un usuario Registrado con ese correo electrónico")    
		##Falta redireccionar bien
    return render(request, "recuperarContra.html")
	
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

def vistaAgendarCita(request):
    especialidadesdb = Especialidad.objects.all()
    especialidades = list()
    for a in especialidadesdb:
        list_Especialidades = {'especialidad':"%s"%(a.nombre)}
        especialidades.append(list_Especialidades)

    return render(request,'AgendarCita_Prueba.html',{'lista_especialidad':especialidades})

especialidad_Escogida = " "

def getEspecialidad(request):
    #print("\n")
    global especialidad_Escogida  #Variable global para filtrar el medico que tenga esa especialidad
    especialidad_Escogida = request.GET['especialidad_categoria']
    #print(request.GET['especialidad_categoria'])
    #print("\n")

    #Se llena la lista con los medicos que tengan una especialidad x
    medico_per_especialidad = getMedicosByEspecialidad() 
    print("------Medicos por especialidad")
    print(medico_per_especialidad)
    print("------Medicos por especialidad")
    return render(request,'AgendarCita_Prueba.html',{'lista_medico':medico_per_especialidad})

def getMedicosByEspecialidad(): #Es llamado en getEspecialidad 
    medicos = Medico.objects.all()
    medicosByEspecialidad = list()
    for filtro in medicos:
        if filtro.especialidad.nombre == especialidad_Escogida:
            print("Entro!!")
            list_Medicos = {'medico':"%s"%(str(filtro.PrimerNombre)+" "+str(filtro.PrimerApellido))}
            medicosByEspecialidad.append(list_Medicos)
    #print(medicosByEspecialidad)
    return medicosByEspecialidad

medico_Escogido = " "

def getMedicos(request):
    global medico_Escogido
    medico_Escogido = request.GET['medico_categoria']
    medico_Escogido = medico_Escogido.split() #Se obtiene una lista con primer nombre y primer apellido del medico
    print("Medico escogido: ",medico_Escogido)

    horarios_medico = getHorarioMedico()
    print("Horario: ",horarios_medico)
    return render(request,'AgendarCita_Prueba.html',{'lista_horario':horarios_medico})

def getHorarioMedico():
    horarios = Horario.objects.all()
    medicos = Medico.objects.filter(PrimerNombre=medico_Escogido[0],PrimerApellido=medico_Escogido[1])
    
    id_horario_medico = ""

    for medicosQuery in medicos: #De momento no encontre una forma eficiente de hacerlo
        id_horario_medico = medicosQuery.horario_id
        
    list_horarios = list()

    for horariosQuery in horarios: 
        if id_horario_medico == horariosQuery.id:
            list_horarios.append(horariosQuery.HorarioLlegada)
            print("query")
            print(horariosQuery.HorarioLlegada)
            list_horarios.append(horariosQuery.HoraioSalida)
    #Obtengo una lista con horario de entrada y salida
    #Tipo de dato -> datetime.time(1, 40, 18)
    
    particionHorarios = list()
    particionHorarios = GenerarHorarioCitas(list_horarios[0],list_horarios[1])
    horarios_Filtrados = list()
    for date in particionHorarios:
        horarios_Filtrados.extend([{'horario':"%s"%(str(date))}])
    return horarios_Filtrados

horario_Escogido = " "

def getHorario(request):
    global horario_Escogido
    horario_Escogido = request.GET['horario_categoria']
    print("Horario_Escogido: ",horario_Escogido)    
    return render(request,'AgendarCita_Prueba.html')

def AgendarCita(request):
    form = AgendarCitaForm()
        
    if request.method == 'POST':
        form = AgendarCitaForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/menu_Paciente/')
        return render(request, 'AgendarCita_Prueba.html', {'form':form})       

    tipoCita = request.GET["tipoCita"] 
    especialidad = request.GET["especialidad"] 
    nmedicos = []
    medicos = Medico.objects.filter(Especialidad=especialidad)
    
    for e in medicos:
        nombre= "%s %s %s %s" %(e.PrimerNombre, e.SegundoNombre, e.PrimerApellido, e.SegundoApellido)
        nmedicos.append(nombre) 

    medico = request.GET["medico"]

    medicoElegido =[]
    temporal=[]
    for e in medico:
        if(e==' '):
            medicoElegido.append(temporal)
            temporal=[]
        else:
            temporal.append(e)
    #EliminarSimbolos(str(medicoElegido))

    medicoBD = Medico.objects.filter (
        PrimerNombre=medicoElegido[0],
        SegundoNombre=medicoElegido[1],
        PrimerApellido=medicoElegido[2],
        SegundoApellido=medicoElegido[3]
        )

    horarioLlegada = medicoBD[0].HorarioLlegada
    horarioSalida = medicoBD[0].HorarioSalida 

    horarios = horarioLlegada

    #horario = request.GET["Horario"]
    #motivoConsulta = request.GET["MotivoDeConsulta"]  
    diccionario ={"medicos":nmedicos, "horarios":horarios}

    return render(request,"principal_Paciente.html",diccionario)
