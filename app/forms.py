from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class UsuarioCreateForm(UserCreationForm):
    telefone = forms.CharField(max_length=15, required=True)
    endereco = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'telefone', 'endereco', 'password1', 'password2')

class UsuarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email', 'telefone', 'endereco')