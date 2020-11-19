from django.shortcuts import render
from qr_code.qrcode.utils import QRCodeOptions

def myview(request):
    context = dict(
        my_options=QRCodeOptions(size='t', border=6, error_correction='L'),
    )

    return render("reas",'./../plantillas/login.html', context=context)