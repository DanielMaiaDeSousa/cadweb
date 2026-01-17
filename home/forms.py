from django import forms
from .models import Cliente, Categoria, Produto


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
        # Certifique-se de que 'img_base64' está na lista de campos:
        fields = ['nome', 'preco', 'categoria', 'img_base64'] 
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'img_base64': forms.HiddenInput(), # Recomendado para Base64
        }