from django import forms

from GestionDeCitas.models import Medico


class UbicacionForm(forms.Form):
    estado = forms.ModelChoiceField(
        label=u'Estado', 
        queryset=Medico.objects.all()
    )
    municipio = forms.ModelChoiceField(
        label=u'Municipio', 
        queryset=Municipio.objects.all()
    )
    localidad = forms.ModelChoiceField(
        label=u'Localidad', 
        queryset=Localidad.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(UbicacionForm, self).__init__(*args, **kwargs)
        self.fields['municipio'].queryset = Municipio.objects.none()
        self.fields['localidad'].queryset = Localidad.objects.none()