from django import forms
from .models import Categoria, Cliente, Produto, Estoque, ItemPedido, Pagamento
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError


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
# home/forms.py

class ItemPedidoForm(forms.ModelForm):
    class Meta:
        model = ItemPedido
        fields = ['produto', 'qtde', 'preco']
        widgets = {
            'produto': forms.HiddenInput(), 
            'qtde': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco': forms.TextInput(attrs={'class': 'money form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ItemPedidoForm, self).__init__(*args, **kwargs)
        self.fields['preco'].localize = True
        self.fields['preco'].widget.is_localized = True

    # --- NOVA VALIDAÇÃO DE ESTOQUE ---
    def clean(self):
        cleaned_data = super().clean()
        produto = cleaned_data.get('produto')
        qtde = cleaned_data.get('qtde')

        if produto and qtde:
            # Busca o estoque vinculado ao produto usando o related_name 'estoque' definido no model
            estoque_obj = produto.estoque.first() 
            
            # Se não existir registro de estoque ou a quantidade for insuficiente
            if not estoque_obj or estoque_obj.quantidade < qtde:
                qtd_disponivel = estoque_obj.quantidade if estoque_obj else 0
                raise forms.ValidationError(
                    f"Estoque insuficiente para o produto {produto.nome}. "
                    f"Quantidade disponível: {qtd_disponivel}."
                )
        
        return cleaned_data        
# home/forms.py

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        # Inclui os novos campos tipo e parcelas para edição
        fields = ['pedido', 'valor', 'forma', 'tipo', 'parcelas']
        widgets = {
            'pedido': forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'valor': forms.TextInput(attrs={'class': 'money form-control', 'id': 'id_valor_pagamento'}),
            'forma': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo_pagamento'}),
            'parcelas': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_parcelas', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        # Aceita um argumento opcional 'pedido' passado pela view para fornecer o débito restante
        self.pedido = kwargs.pop('pedido', None)
        super(PagamentoForm, self).__init__(*args, **kwargs)

        # Formatação/localização do campo valor
        self.fields['valor'].localize = True
        self.fields['valor'].widget.is_localized = True

        # Se receber o pedido, define o atributo data-debito no widget do campo 'valor'
        if self.pedido is not None:
            try:
                debito = self.pedido.debito_restante
                # Garante que o atributo exista para uso pelo JS (usar ponto decimal para parseFloat)
                self.fields['valor'].widget.attrs['data-debito'] = str(debito if debito is not None else 0)
            except Exception:
                # Segurança: não quebra caso o pedido não tenha o atributo
                pass

        # Garante valores iniciais para campos quando instanciação com 'instance' for usada
        if self.instance and self.instance.pk:
            # Ajusta id do campo parcelas caso exista instância
            self.fields['parcelas'].initial = self.instance.parcelas
            self.fields['tipo'].initial = self.instance.tipo
            self.fields['valor'].initial = self.instance.valor
            self.fields['forma'].initial = self.instance.forma

    def clean_valor(self):
        """Converte o valor com vírgula para Decimal e valida limites."""
        raw = self.cleaned_data.get('valor')

        # Se já veio como Decimal, retornamos sem alterações
        if isinstance(raw, Decimal):
            valor = raw
        else:
            # Pode vir como string com vírgula (e.g. '1.234,56')
            if raw is None:
                raise ValidationError("Informe o valor do pagamento.")
            # Normaliza: remove pontos de milhar e troca vírgula por ponto
            texto = str(raw).replace('.', '').replace(',', '.')
            try:
                valor = Decimal(texto)
            except (InvalidOperation, ValueError):
                raise ValidationError("Valor inválido.")

        if valor <= 0:
            raise ValidationError("O valor do pagamento deve ser maior que zero.")

        # Se tivermos um pedido, não permita pagar mais que o débito restante
        if hasattr(self, 'pedido') and self.pedido is not None:
            if valor > Decimal(str(self.pedido.debito_restante)):
                raise ValidationError(f"O valor (R$ {valor:.2f}) excede o débito restante (R$ {self.pedido.debito_restante:.2f}).")

        return valor

    def clean_parcelas(self):
        parcelas = self.cleaned_data.get('parcelas')
        tipo = self.data.get('tipo') # Pega o dado bruto do POST para conferir o tipo

    # Se for à vista, ignoramos o que vier no campo parcelas e forçamos 1
        if tipo == 'a_vista':
            return 1
    
        if not parcelas or int(parcelas) < 1:
            raise ValidationError('Para pagamentos parcelados, informe o número de parcelas (mínimo 1).')
    
        return parcelas

    def clean(self):
        cleaned = super().clean()
        tipo = cleaned.get('tipo')
    
    # Se não for parcelado, garantimos que o sistema entenda como 1 parcela
        if tipo != 'parcelado':
            cleaned['parcelas'] = 1
        
        return cleaned