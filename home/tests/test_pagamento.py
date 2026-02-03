from django.test import TestCase, Client
from django.urls import reverse
from home.forms import PagamentoForm
from home.models import Cliente, Produto, Pedido, ItemPedido, Pagamento, Estoque
from decimal import Decimal

class PagamentoFormTests(TestCase):
    def setUp(self):
        self.cliente = Cliente.objects.create(nome='Cliente Teste', cpf='000.000.000-00', datanasc='1990-01-01')
        self.categoria = None
        # cria categoria mínima para a FK
        from home.models import Categoria
        self.categoria = Categoria.objects.create(nome='Cat Teste', ordem=1)
        self.produto = Produto.objects.create(nome='Produto 1', preco=Decimal('100.00'), categoria=self.categoria)
        self.pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=self.pedido, produto=self.produto, qtde=1, preco=Decimal('100.00'))

    def test_valor_com_virgula_aceito(self):
        form = PagamentoForm(data={
            'valor': '1.234,56',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertTrue(form.is_valid())
        pagamento = form.save(commit=False)
        self.assertEqual(pagamento.valor, Decimal('1234.56'))

    def test_valor_maior_que_debito_rejeitado(self):
        # Débito do pedido é 100.00
        form = PagamentoForm(data={
            'valor': '200,00',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)
        self.assertTrue(any('excede o débito restante' in e for e in form.errors['valor']))

    def test_parcelas_invalidas(self):
        form = PagamentoForm(data={
            'valor': '50,00',
            'forma': 'dinheiro',
            'tipo': 'parcelado',
            'parcelas': 0,
            'pedido': self.pedido.id
        }, pedido=self.pedido)
        self.assertFalse(form.is_valid())
        self.assertIn('parcelas', form.errors)

class RegistrarPagamentoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(nome='Cliente Teste 2', cpf='111.111.111-11', datanasc='1990-01-01')
        self.produto = Produto.objects.create(nome='Produto 2', preco=Decimal('50.00'), categoria=1)
        self.pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=self.pedido, produto=self.produto, qtde=2, preco=Decimal('50.00'))

    def test_post_valido_cria_pagamento(self):
        url = reverse('registrar_pagamento', args=[self.pedido.id])
        response = self.client.post(url, data={
            'valor': '50,00',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        # Redireciona após sucesso
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Pagamento.objects.filter(pedido=self.pedido).count(), 1)

    def test_pagamento_quita_pedido_baixa_estoque_e_fecha_pedido(self):
        # cria um estoque inicial e faz o pagamento total
        Estoque.objects.create(produto=self.produto, quantidade=5)
        url = reverse('registrar_pagamento', args=[self.pedido.id])
        response = self.client.post(url, data={
            'valor': '100,00',
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        self.assertEqual(response.status_code, 302)
        estoque = Estoque.objects.get(produto=self.produto)
        # 5 - 2 (qtde do ItemPedido) = 3
        self.assertEqual(estoque.quantidade, 3)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.status, 3)

    def test_post_invalido_reexibe_form_com_erro(self):
        url = reverse('registrar_pagamento', args=[self.pedido.id])
        response = self.client.post(url, data={
            'valor': '1000,00',  # excede o débito
            'forma': 'dinheiro',
            'tipo': 'a_vista',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        # Deve reexibir a página com erros (status 200)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'excede o débito restante')


class EditarPagamentoViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.cliente = Cliente.objects.create(nome='Cliente Edit', cpf='222.222.222-22', datanasc='1990-01-01')
        from home.models import Categoria
        self.categoria = Categoria.objects.create(nome='Cat Edit', ordem=1)
        self.produto = Produto.objects.create(nome='Produto Edit', preco=Decimal('25.00'), categoria=self.categoria)
        self.pedido = Pedido.objects.create(cliente=self.cliente)
        ItemPedido.objects.create(pedido=self.pedido, produto=self.produto, qtde=1, preco=Decimal('25.00'))
        self.pagamento = Pagamento.objects.create(pedido=self.pedido, valor=Decimal('25.00'), forma='dinheiro', tipo='a_vista', parcelas=1)

    def test_post_edit_with_hidden_fields_updates(self):
        url = reverse('editar_pagamento', args=[self.pagamento.id])
        response = self.client.post(url, data={
            'valor': '30,00',
            # omit 'forma' and 'tipo' to simulate selects not being sent by the browser
            'parcelas': 1,
            'hidden_forma': 'pix',
            'hidden_tipo': 'a_vista',
            'pedido': self.pedido.id
        })
        # deve redirecionar após sucesso
        self.assertEqual(response.status_code, 302)
        self.pagamento.refresh_from_db()
        self.assertEqual(self.pagamento.forma, 'pix')
        self.assertEqual(self.pagamento.tipo, 'a_vista')
        self.assertEqual(self.pagamento.valor, Decimal('30.00'))

    def test_post_edit_without_hidden_fails(self):
        url = reverse('editar_pagamento', args=[self.pagamento.id])
        response = self.client.post(url, data={
            'valor': '30,00',
            'parcelas': 1,
            'pedido': self.pedido.id
        })
        # Deve reexibir a página com erro (status 200) e mensagem de campo obrigatório
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este campo é obrigatório')