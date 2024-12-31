# models.py
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from decimal import Decimal
from django.conf import settings

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=15)
    endereco = models.TextField()
    is_cliente = models.BooleanField(default=True)
    is_funcionario = models.BooleanField(default=False)

    class Meta:
        permissions = [
            ("pode_gerenciar_pedidos", "Pode gerenciar pedidos"),
            ("pode_gerenciar_cardapio", "Pode gerenciar cardápio"),
        ]

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/', blank=True)
    disponivel = models.BooleanField(default=True)
    permite_complementos = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Complemento(models.Model):
    nome = models.CharField(max_length=100)
    preco_adicional = models.DecimalField(max_digits=10, decimal_places=2)
    produtos = models.ManyToManyField(Produto, related_name='complementos_disponiveis')
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('saiu_entrega', 'Saiu para Entrega'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    endereco_entrega = models.TextField()
    observacoes = models.TextField(blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Pedido #{self.id} - {self.cliente.username}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(blank=True)

    def subtotal(self):
        return self.quantidade * self.preco_unitario

class ItemComplemento(models.Model):
    item_pedido = models.ForeignKey(ItemPedido, related_name='complementos', on_delete=models.CASCADE)
    complemento = models.ForeignKey(Complemento, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

# Carrinho de Compras
class CarrinhoCompra(models.Model):
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

class ItemCarrinho(models.Model):
    carrinho = models.ForeignKey(CarrinhoCompra, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    observacao = models.TextField(blank=True)

class ComplementoCarrinho(models.Model):
    item_carrinho = models.ForeignKey(ItemCarrinho, related_name='complementos', on_delete=models.CASCADE)
    complemento = models.ForeignKey(Complemento, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)