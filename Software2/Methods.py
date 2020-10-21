import mysql.connector
from mysql.connector import errorcode
import random

def EliminarSimbolos(x):
	x = str(x).replace("'","").replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace(" ","")
	return x

def CursorDB(cnx):
	Cursor = cnx.cursor()
	return Cursor

def DefinirCondiciónMedica(condicion):
	if condicion=='si':
		return True
	else:
		return False

def GenerateUserByCorreoElement(email):
	userArray=[]
	passwordArray=[]
	for e in email:
		if e == '@' or e=='.' :
			pass
		else:
			if email.index(e) % 2 ==0:
				passwordArray.append(e)
			else:
				userArray.append(e)
	random.shuffle(userArray)
	random.shuffle(passwordArray)
	
	User = [EliminarSimbolos(userArray),EliminarSimbolos(passwordArray)] 
	return User

def CampoOpcional(request, campo):
	if request.GET[campo]:
		variable = request.GET[campo]
	else:
		variable = ''
	return variable	





