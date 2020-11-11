from django import forms
from GestionDeCitas.models import Especialidad

class AgregarMedicoForm(forms.Form):
    especialidades = forms.ModelChoiceField(
        label=u'especialidad', 
        queryset = Especialidad.objects.values_list('nombre',flat=True),widget=forms.Select(attrs={
        'class': 'form-control', 'id':'especialidad'
    }))