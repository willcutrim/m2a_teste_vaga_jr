from django import forms
from .models import Abastecimento, PrecoCombustivel, Posto, Bomba, Tanque

class AbastecimentoForm(forms.ModelForm):
    class Meta:
        model = Abastecimento
        fields = ['bomba', 'litros'] 


class PrecoCombustivelForm(forms.ModelForm):
    class Meta:
        model = PrecoCombustivel
        fields = ['tipo_combustivel', 'preco_por_litro']


class PostoForm(forms.ModelForm):
    class Meta:
        model = Posto
        fields = ['nome']

class BombaForm(forms.ModelForm):
    class Meta:
        model = Bomba
        fields = ['identificacao', 'tanque']

class TanqueForm(forms.ModelForm):
    class Meta:
        model = Tanque
        fields = ['tipo_combustivel', 'capacidade', 'posto']