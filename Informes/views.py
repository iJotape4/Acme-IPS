from django.shortcuts import render

# Create your views here.
lista = [1,2,3,4]

def informe_Ips(request):
	return render(request, "./informe_IPS.html",{"lista":lista})