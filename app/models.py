from django.db import models
from django.contrib.auth.models import User


#Área do admin
#obs: adcionar os tamanhos para as bebidas, como 1l , 600ml, etc.

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(upload_to='image/%Y/%m', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
    
    
class Complemento(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nome

class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    complemento = models.ForeignKey(Complemento, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'Item - {self.produto.nome}'


#Área do cliente
class Carrinho(models.Model):
    itens = models.ManyToManyField(ItemCarrinho)

    def __str__(self):
        return 'Carrinho'

class Pedido(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Pedido'