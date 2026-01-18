from django import forms
from .models import Categoria, Cliente, Produto
from django.utils import timezone

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control'}),
            'datanasc': forms.DateInput(attrs={'class': 'data form-control', 'type': 'date'}),
        }

    def clean_datanasc(self):
        # TAREFA: Impede data de nascimento no futuro
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > timezone.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")
        return datanasc

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'img_base64': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        # TAREFA: Formata o preço na inicialização
        super(ProdutoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.preco:
            valor = "{:,.2f}".format(self.instance.preco).replace(",", "X").replace(".", ",").replace("X", ".")
            self.initial['preco'] = valor