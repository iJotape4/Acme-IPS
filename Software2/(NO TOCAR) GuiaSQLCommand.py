from django.db import models
import mysql.connector
from mysql.connector import errorcode

# Create your models here.
#Execute --> pip install mysql-connector-python
try:
    cnx = mysql.connector.connect(user='root', password='Sistemas132',host='127.0.0.1',database='dbipsacme')
    print("Conexion establecida")
    cursor = cnx.cursor()

    query = ("SELECT * FROM paciente")

    consulta = cursor.execute(query)

    for i in cursor:
        print(i)
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor.close()
    cnx.close()

