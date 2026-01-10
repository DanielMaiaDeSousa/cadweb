#from django import forms
#from .models import *
from django import forms
from .models import Categoria  # Certifique-se de que o modelo foi importado

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria  # ESTA LINHA É OBRIGATÓRIA
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': ''}),
        }

    # Validação personalizada para o nome
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    # Validação personalizada para a ordem
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem is not None and ordem <= 0:
            raise forms.ValidationError("O campo ordem deve ser maior que zero.")
        return ordem