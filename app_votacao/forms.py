from django.forms import ModelForm
from .models import UsuarioPerfil, Candidatos, Votacao
from localflavor.br.forms import BRCPFField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistroUsuario(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Lembre-se que o seu usuário lhe concederá acesso ao sistema.',
        }

class UsuarioPerfilForm(ModelForm):
    cpf = BRCPFField()
    class Meta:
        model = UsuarioPerfil
        fields = ('cpf', 'biografia')

class CandidatosForm(ModelForm):
    class Meta:
        model = Candidatos
        fields = ('nome', 'biografia', 'imagem')

class VotacaoForm(ModelForm):
    class Meta:
        model = Votacao
        fields = ('nome', 'candidato1', 'candidato2', 'status')



