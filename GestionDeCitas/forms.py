from django import forms
from GestionDeCitas.models import Medico,Especialidad, Horario

class AgendarCitaForm(forms.Form):
    especialidades = forms.ModelChoiceField(
        label=u'especialidad', 
        queryset = Especialidad.objects.values_list('nombre',flat=True),widget=forms.Select(attrs={
        'class': 'form-control', 'disabled':'true', 'id':'especialidad'
    }))
    
    medicos = forms.ModelChoiceField(
        label=u'medico', 
        queryset = Medico.objects.none(),widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    horarios = forms.ModelChoiceField(
        label=u'horario', 
        queryset = Horario.objects.none(),widget=forms.Select(attrs={
        'class': 'form-control'
    }))
