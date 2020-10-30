#Instalar --> python -m pip install reportlab

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

#Documentacion -> https://docs.djangoproject.com/en/3.1/howto/outputting-pdf/

def pdfGenerator(request,directorio):
    try:
        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas("hello.pdf")

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
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