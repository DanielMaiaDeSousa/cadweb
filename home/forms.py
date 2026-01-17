from django import forms
from .models import Cliente, Categoria, Produto
from django.utils import timezone


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da Categoria'}),
            'ordem': forms.NumberInput(attrs={'class': 'inteiro form-control', 'placeholder': 'Ordem da Categoria'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')

        if ordem is not None and ordem < 0:
            raise forms.ValidationError("A ordem deve ser um número inteiro positivo.")
        return ordem

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Cliente'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'C.P.F do Cliente'}),       
            'datanasc': forms.DateInput(format='%d/%m/%Y', attrs={'class': 'data form-control', 'placeholder': 'Data de Nascimento (DD/MM/AAAA)'}),
            
        }
    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > timezone.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser maior que a data atual.")
        return datanasc
        
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria','img_base64']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'nome':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'img_base64': forms.HiddenInput(), 
            # a classe money mascara a entreda de valores monetários, está em base.html
            #  jQuery Mask Plugin
            'preco':forms.TextInput(attrs={
                'class': 'money form-control',
                'maxlength': 500,
                'placeholder': '0.000,00'
            }),
        }
        
        labels = {
            'nome': 'Nome do Produto',
            'preco': 'Preço do Produto',
        }


    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.preco:
            # Formata para o campo de edição aparecer com vírgula
            valor = "{:,.2f}".format(self.instance.preco).replace(",", "X").replace(".", ",").replace("X", ".")
            self.initial['preco'] = valor