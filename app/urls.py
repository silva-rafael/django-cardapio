# urls.py
from django.urls import path
from . import views
from .views import CustomLoginView, RegisterView, profile_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.CardapioListView.as_view(), name='cardapio'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_ao_carrinho, name='adicionar_ao_carrinho'),
    path('carrinho/', views.ver_carrinho, name='ver_carrinho'),
    path('pedido/finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('admin/painel/', views.painel_admin, name='painel_admin'),
    path('admin/pedido/<int:pedido_id>/status/', views.atualizar_status_pedido, name='atualizar_status_pedido'),
    
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', profile_view, name='profile'),
    path('accounts/profile/', profile_view, name='profile'),
]
