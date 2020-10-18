import mysql.connector
from mysql.connector import errorcode

def EliminarSimbolos(x):
	x = str(x).replace("'","").replace("(","").replace(")","").replace(",","")
	return x

def CursorDB(cnx):
	Cursor = cnx.cursor()
	return Cursor