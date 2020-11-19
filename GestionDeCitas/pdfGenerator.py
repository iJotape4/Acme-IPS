import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def pdfGenerator(request,directorio):
    try:
        p = canvas.Canvas("hello.pdf")
        p.drawString(100, 100, )

        p.showPage()
        p.save()

    except Exception as e:
        print("Ha ocurrido un error durante la generación del PDF -> {}".format(e))

