# Generated by Django 5.1.4 on 2024-12-31 12:01

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Complemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco_adicional', models.DecimalField(decimal_places=2, max_digits=10)),
                ('disponivel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observacao', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefone', models.CharField(max_length=15)),
                ('endereco', models.TextField()),
                ('is_cliente', models.BooleanField(default=True)),
                ('is_funcionario', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': [('pode_gerenciar_pedidos', 'Pode gerenciar pedidos'), ('pode_gerenciar_cardapio', 'Pode gerenciar cardápio')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CarrinhoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('observacao', models.TextField(blank=True)),
                ('carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='app.carrinhocompra')),
            ],
        ),
        migrations.CreateModel(
            name='ComplementoCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('complemento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.complemento')),
                ('item_carrinho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complementos', to='app.itemcarrinho')),
            ],
        ),
        migrations.CreateModel(
            name='ItemComplemento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('preco_unitario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('complemento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.complemento')),
                ('item_pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='complementos', to='app.itempedido')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_pedido', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('confirmado', 'Confirmado'), ('preparando', 'Preparando'), ('saiu_entrega', 'Saiu para Entrega'), ('entregue', 'Entregue'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('endereco_entrega', models.TextField()),
                ('observacoes', models.TextField(blank=True)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='itempedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='app.pedido'),
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagem', models.ImageField(blank=True, upload_to='produtos/')),
                ('disponivel', models.BooleanField(default=True)),
                ('permite_complementos', models.BooleanField(default=False)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.categoria')),
            ],
        ),
        migrations.AddField(
            model_name='itempedido',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.produto'),
        ),
        migrations.AddField(
            model_name='itemcarrinho',
            name='produto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.produto'),
        ),
        migrations.AddField(
            model_name='complemento',
            name='produtos',
            field=models.ManyToManyField(related_name='complementos_disponiveis', to='app.produto'),
        ),
    ]
