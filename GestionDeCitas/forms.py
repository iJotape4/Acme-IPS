from django import forms
from GestionDeCitas.models import Medico,Especialidad, Horario

class AgendarCitaForm(forms.Form):
    especialidades = forms.ModelChoiceField(
        label=u'especialidad', 
        queryset = Especialidad.objects.values_list('nombre',flat=True),widget=forms.Select(attrs={
        'class': 'form-control'
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
    
    """
    .values('PrimerNombre','PrimerApellido')
    
    horario = forms.ModelChoiceField(
        label=u'horario', 
        queryset=Horario.objects.all(),widget=forms.Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    })
    )

    def __init__(self, *args, **kwargs):
        super(AgendarCitaForm, self).__init__(*args, **kwargs)
        self.fields['medico'].queryset = Medico.objects.none()
        self.fields['horario'].queryset = Horario.objects.none()"""