#Instalar --> pip install django-qr-code
#Documentacion --> https://django-qr-code.readthedocs.io/en/latest/pages/README.html#usage
"""Colocar en settings.py --> 
INSTALLED_APPS = (
    'qr_code',
)
"""

from django.shortcuts import render
from qr_code.qrcode.utils import QRCodeOptions

def myview(request):
    # Build context for rendering QR codes.
    context = dict(
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )

    # Render the view.
    return render("reas",'./../plantillas/login.html', context=context)