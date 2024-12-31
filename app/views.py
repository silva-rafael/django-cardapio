# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UsuarioCreateForm, UsuarioUpdateForm
from django.contrib.auth.views import LoginView


class CustomLoginView(LoginView):
    template_name = 'app/login.html'
    redirect_authenticated_user = True

class RegisterView(CreateView):
    form_class = UsuarioCreateForm
    template_name = 'app/register.html'
    success_url = reverse_lazy('cardapio')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UsuarioUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UsuarioUpdateForm(instance=request.user)
    
    return render(request, 'app/profile.html', {'form': form})
#-----------------------------------------------------------------------

# Views para o Cliente
class CardapioListView(ListView):
    model = Produto
    template_name = 'app/cardapio.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        return Produto.objects.filter(disponivel=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.filter(ativo=True)
        return context

@login_required
def adicionar_ao_carrinho(request, produto_id):
    if request.method == 'POST':
        produto = get_object_or_404(Produto, id=produto_id, disponivel=True)
        carrinho, criado = CarrinhoCompra.objects.get_or_create(cliente=request.user)
        
        quantidade = int(request.POST.get('quantidade', 1))
        observacao = request.POST.get('observacao', '')
        
        item = ItemCarrinho.objects.create(
            carrinho=carrinho,
            produto=produto,
            quantidade=quantidade,
            observacao=observacao
        )
        
        # Processar complementos
        complementos = request.POST.getlist('complementos')
        for comp_id in complementos:
            complemento = get_object_or_404(Complemento, id=comp_id)
            ComplementoCarrinho.objects.create(
                item_carrinho=item,
                complemento=complemento,
                quantidade=1
            )
            
        return redirect('ver_carrinho')

@login_required
def ver_carrinho(request):
    carrinho, criado = CarrinhoCompra.objects.get_or_create(cliente=request.user)
    return render(request, 'app/carrinho.html', {'carrinho': carrinho})

@login_required
def finalizar_pedido(request):
    if request.method == 'POST':
        carrinho = get_object_or_404(CarrinhoCompra, cliente=request.user)
        
        # Criar pedido
        pedido = Pedido.objects.create(
            cliente=request.user,
            endereco_entrega=request.POST['endereco'],
            observacoes=request.POST.get('observacoes', ''),
            valor_total=0  # Será calculado abaixo
        )
        
        valor_total = 0
        
        # Transferir itens do carrinho para o pedido
        for item_carrinho in carrinho.itens.all():
            item_pedido = ItemPedido.objects.create(
                pedido=pedido,
                produto=item_carrinho.produto,
                quantidade=item_carrinho.quantidade,
                preco_unitario=item_carrinho.produto.preco,
                observacao=item_carrinho.observacao
            )
            
            # Transferir complementos
            for comp_carrinho in item_carrinho.complementos.all():
                ItemComplemento.objects.create(
                    item_pedido=item_pedido,
                    complemento=comp_carrinho.complemento,
                    quantidade=comp_carrinho.quantidade,
                    preco_unitario=comp_carrinho.complemento.preco_adicional
                )
            
            # Calcular subtotal
            subtotal = (item_pedido.preco_unitario * item_pedido.quantidade)
            valor_total += subtotal
        
        # Atualizar valor total do pedido
        pedido.valor_total = valor_total
        pedido.save()
        
        # Limpar carrinho
        carrinho.delete()
        
        return redirect('pedido_confirmado', pedido_id=pedido.id)

# Views para o Admin
@login_required
def painel_admin(request):
    if not request.user.is_staff:
        return redirect('home')
    
    pedidos_pendentes = Pedido.objects.filter(status='pendente').order_by('-data_pedido')
    return render(request, 'admin/painel.html', {
        'pedidos_pendentes': pedidos_pendentes
    })

@login_required
def atualizar_status_pedido(request, pedido_id):
    if not request.user.is_staff:
        return redirect('home')
        
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        novo_status = request.POST.get('status')
        if novo_status in dict(Pedido.STATUS_CHOICES):
            pedido.status = novo_status
            pedido.save()
    
    return redirect('painel_admin')

