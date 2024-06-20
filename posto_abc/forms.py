# forms.py
from django import forms
from .models import Abastecimento

class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = ['bomba', 'litros']  
