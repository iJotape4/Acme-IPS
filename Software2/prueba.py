import random
def GenerateUserByCorreoElement(email):
	userArray=[]
	passwordArray=[]
	for e in email:
		#print("indeX"+str(e.index()))
		if email.index(e) % 2 ==0:
			passwordArray.append(e)
		else:
			userArray.append(e)
	random.shuffle(userArray)
	random.shuffle(passwordArray)	

	print(str(userArray).replace("'","").replace("(","").replace(")","").replace(",","").replace("[","").replace("]","").replace(" ",""))
	print(passwordArray)

GenerateUserByCorreoElement("holandas")	