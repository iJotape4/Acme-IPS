from datetime import date, datetime
#from Software2.Methods import EliminarSimbolos

def EliminarSimbolos(x):
	x = str(x).replace("'","").replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace(" ","")
	return x

def FormatFecha(date):

	fecha = date.split('/')
	
	invertir = [fecha[2], '/', fecha[1],'/', fecha[0]]

	formatear = datetime.strptime(EliminarSimbolos(str(invertir)),"%Y/%m/%d").date()

	return formatear			

#print(FormatFecha("17/10/2020"))
#print(datetime.strptime("2020/10/17","%Y/%m/%d")

def Programada(date, hora):
	date = datetime(date.year, date.month, date.day, hora.hour, hora.minute, hora.second, hora.microsecond)
	if date > datetime.now():
		return true
	else:
		return false	

Programada(datetime.now().date(), datetime.now().time())	