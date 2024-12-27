# Generated by Django 5.1.4 on 2024-12-27 16:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrinho',
            name='complementos',
        ),
        migrations.RemoveField(
            model_name='carrinho',
            name='produtos',
        ),
        migrations.RemoveField(
            model_name='complemento',
            name='produto',
        ),
        migrations.CreateModel(
            name='ItemCarrinho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complemento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.complemento')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.produto')),
            ],
        ),
        migrations.AddField(
            model_name='carrinho',
            name='itens',
            field=models.ManyToManyField(to='app.itemcarrinho'),
        ),
    ]