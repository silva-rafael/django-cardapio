from django.contrib import admin
from .models import *

admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Carrinho)
admin.site.register(Complemento)
admin.site.register(Categoria)
admin.site.register(ItemCarrinho)
