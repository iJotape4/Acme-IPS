from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from Software2.Methods import DefinirCondiciónMedica, CampoOpcional, EliminarSimbolos 
from Software2.Methods import send_email, GenerarHorarioCitas
from django.contrib import messages
from django import forms
from django.http import JsonResponse
from GestionDeCitas.models import Paciente, Medico,Horario,Especialidad,Cita
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from GestionDeCitas.models import Medico
from GestionDeCitas.forms import AgendarCitaForm

class AgendarCitaView(TemplateView):
    template_name = 'AgendarCita_Prueba.html'

    especialidad_AJAX = ""
    medico_AJAX = ""
    horario_AJAX = ""

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        print("\n")
        print("Haciendo POST -> ",request.POST)
        print("\n")
        try:
            respuesta = list(request.POST.values())
            action = respuesta[0]
            if action == 'buscar_medico_por_especialidad':
                data = AgendarCitaView.filtrar_Medicos(self,data,respuesta)
            elif action == 'buscar_horario_por_medico':
                data = AgendarCitaView.filtrar_Horarios(self,data,respuesta)
            elif action == 'horario_seleccionado':
                pass
            else:   
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        finally:
            return JsonResponse(data,safe=False)

    def filtrar_Medicos(self,data,respuesta):
       
        print("\n Filtrar Medicos")
        print(respuesta)
        print("\n")
        especialidad = respuesta[1]
        AgendarCitaView.especialidad_AJAX = especialidad

        especialidad_AJAX = especialidad
        id_especialidad_Escogida = list(Especialidad.objects.filter(nombre=especialidad).values_list('id',flat=True))
        
        filtro = list(Medico.objects.filter(especialidad_id=id_especialidad_Escogida[0]).values())
        for dato in filtro:
            data.append({'PrimerNombre': dato['PrimerNombre'],'PrimerApellido':dato['PrimerApellido']})
        return data

    def filtrar_Horarios(self,data,respuesta):
        print("\n Filtrar horarios")
        print(respuesta)
        print("\n")
        medico = respuesta[1]
        AgendarCitaView.medico_AJAX = medico

        id_Horario_Escogido = list(Medico.objects.filter(PrimerNombre=medico).values_list('horario_id',flat=True))
        print(id_Horario_Escogido)
        filtro = list(Horario.objects.filter(id=id_Horario_Escogido[0]).values())
        print("\n print del filtro",filtro,"\n")
        #data.extend(GenerarHorarioCitas(filtro[0]['HorarioLlegada'],filtro[0]['HoraioSalida']))
        #print(data)
        data.append({"Horarios":"10:58"})
        #for dato in filtro:
        #    print(GenerarHorarioCitas(dato['HorarioLlegada'],dato['HoraioSalida']))
            #data.append({'Horarios':GenerarHorarioCitas(dato['HorarioLlegada'],dato['HoraioSalida'])})
            #data.append({'HorarioEntrada': dato['PrimerNombre'],'HorarioSalida':dato['PrimerApellido']})
        return data
        #for date in particionHorarios:
        #horarios_Filtrados.extend([{'horario':"%s"%(str(date))}])"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AgendarCitaForm()
        return context

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

def selectFecha(request):
    print("--------------------")
    print(request.GET.get('fecha'))
    print("--------------------")
    return login(request) 

def logearse(request):
    global nombre
    #global nombre_Usuario
    #global is_logged_in 
    #El if comprueba si los campos están llenos
    if request.GET["username"] and request.GET["password"]:
        #Esto recupera los datos en los campos
        usuario = request.GET["username"]
        contra = request.GET["password"] 

        #Esto busca en la base de datos ese usuario y contraseña
        user = Paciente.objects.filter(Usuario=usuario, Contraseña=contra)
        for e in user:
            nombre = "%s %s" %(e.PrimerNombre, e.PrimerApellido)            

        #Esto condiciona a que ambos existan y coincidan
        if user:   
            #nombre_Usuario = nombre
            #is_logged_in = True 
            request.session['usuario'] = request.GET['username'] #Se crea una session en la bd con la sesion actual
            print("usuario logueado -->",request.session['usuario']) 
            print('logeado: ',request.session['usuario'])
            return render_Menu_Paciente(request,{"userlogeado":nombre,'logeado':request.session['usuario']})
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
            messages.warning(request, "No existe un usuario Registrado con ese correo electrónico") 
            return render(request, "recuperarContra.html")   
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
