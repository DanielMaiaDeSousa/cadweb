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

# home/forms.py

# home/forms.py
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': '000.000.000-00'}),       
            # Mudamos para TextInput para a máscara .data do seu base.html funcionar
            'datanasc': forms.TextInput(attrs={
                'class': 'data form-control', 
                'placeholder': 'DD/MM/AAAA'
            }),
        }

    def clean_datanasc(self):
        # TAREFA: Impede data de nascimento no futuro
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > timezone.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")
        return datanasc

# No arquivo home/forms.py

# home/forms.py
# home/forms.py
from django import forms
from .models import Categoria, Cliente, Produto
from django.utils import timezone

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            # OBRIGATÓRIO: usar TextInput para a máscara não conflitar
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'img_base64': forms.HiddenInput(),
        }

    def clean_preco(self):
        # Pega o valor que veio do formulário (ex: "1.250,50")
        preco = self.request.POST.get('preco') if hasattr(self, 'request') else self.cleaned_data.get('preco')
        
        # Se o preco vier como string do POST, limpamos a formatação brasileira
        if isinstance(preco, str):
            preco = preco.replace('.', '').replace(',', '.')
        
        try:
            return float(preco)
        except (ValueError, TypeError):
            raise forms.ValidationError("Formato de preço inválido.")

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.preco:
            # Formata para o campo de edição (Tarefa do professor)
            valor = "{:,.2f}".format(self.instance.preco).replace(",", "X").replace(".", ",").replace("X", ".")
            self.initial['preco'] = valor