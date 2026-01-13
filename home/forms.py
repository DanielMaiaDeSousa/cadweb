from django import forms
from .models import Categoria, Cliente, Produto  # Certifique-se de que os modelos foram importados

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
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control'}),
            'datanasc': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'data form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
        }