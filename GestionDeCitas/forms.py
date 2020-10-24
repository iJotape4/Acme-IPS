from django import forms

from GestionDeCitas.models import Medico,Especialidad, Horario


class AgendarCitaForm(forms.Form):
    especialidad = forms.ModelChoiceField(
        label=u'especialidad', 
        queryset=Especialidad.objects.all()
    )
    medico = forms.ModelChoiceField(
        label=u'medico', 
        queryset=Medico.objects.all()
    )
    horario = forms.ModelChoiceField(
        label=u'horario', 
        queryset=Horario.objects.all()
    )

    def __init__(self, *args, **kwargs):
        super(AgendarCitaForm, self).__init__(*args, **kwargs)
        self.fields['medico'].queryset = Medico.objects.none()
        self.fields['horario'].queryset = Horario.objects.none()