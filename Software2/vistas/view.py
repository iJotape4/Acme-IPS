from django.http import HttpResponse

def saludo(request):

    return HttpResponse("<html><body><h1>Hola mundo</h1></body></html>")

def despedida(request):

    return HttpResponse("<html><body><h1>El programa se despide</h1></body></html>")