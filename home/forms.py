from django import forms
from .models import Categoria, Cliente, Produto, Estoque, ItemPedido, Pagamento
from django.utils import timezone
# home/views.py
from .models import Categoria, Cliente, Produto, Estoque, Pedido, ItemPedido, Pagamento # Adicione Pagamento aqui
from .forms import CategoriaForm, ClienteForm, ProdutoForm, EstoqueForm, ItemPedidoForm, PagamentoForm # Adicione PagamentoForm aqui

# --- CATEGORIA ---
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'ordem': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
    def clean_nome(self): # Corrigido de clean_ordem para clean_nome
        nome = self.cleaned_data.get('nome')
        if nome and len(nome) < 3:   
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        if ordem is not None and ordem < 0:
            raise forms.ValidationError("A ordem deve ser um número positivo.")
        return ordem

# --- CLIENTE ---
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'cpf', 'datanasc']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': '000.000.000-00'}),       
            'datanasc': forms.TextInput(attrs={
                'class': 'data form-control', 
                'placeholder': 'DD/MM/AAAA'
            }),
        }

    def clean_datanasc(self):
        datanasc = self.cleaned_data.get('datanasc')
        if datanasc and datanasc > timezone.now().date():
            raise forms.ValidationError("A data de nascimento não pode ser no futuro.")
        return datanasc

# --- PRODUTO ---
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'categoria', 'img_base64']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
            'categoria': forms.HiddenInput(), # Atividade 15: Autocomplete 
            'img_base64': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ProdutoForm, self).__init__(*args, **kwargs)
        # Ativa localização para tratar vírgulas e pontos nativamente
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True

# --- ESTOQUE (Atividade 14) ---
class EstoqueForm(forms.ModelForm):
    class Meta:
        model = Estoque
        fields = ['quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# --- ITEM PEDIDO (Atividade 17) ---
class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'qtde', 'preco']
        widgets = {
            # Atividade 17: O campo produto é hidden para o autocomplete 
            'produto': forms.HiddenInput(), 
            'qtde': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(ItemPedidoForm, self).__init__(*args, **kwargs)
        # Ativa localização para tratar vírgulas e pontos nativamente
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True
        
# home/forms.py

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = ['pedido', 'valor', 'forma']
        widgets = {
            'pedido': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'valor': forms.TextInput(attrs={'class': 'money form-control'}),
            'forma': forms.Select(attrs={'class': 'form-control'}),
        }