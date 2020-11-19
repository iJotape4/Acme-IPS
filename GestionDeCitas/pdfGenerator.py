import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def pdfGenerator(request,directorio):
    try:
        p = canvas.Canvas("hello.pdf")
        p.drawString(100, 100, )

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        #buffer.seek(0)
        #return FileResponse(as_attachment=True, filename='hello.pdf')
    except Exception as e:
        print("Ha ocurrido un error durante la generación del PDF -> {}".format(e))

pdfGenerator()