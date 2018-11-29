from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Votacao, Candidatos, Voto, UsuarioPerfil
from django.contrib.auth import login, authenticate, logout
from .forms import RegistroUsuario, UsuarioPerfilForm
# Create your views here.


def inicial(request):
    if request.user.is_authenticated:
        pass
    else:
        messages.warning(request, 'Você precisa estar autenticado para participar de uma votação!')

    votacoes = Votacao.objects.all()
    return render(request, 'site/inicial.html', {'votacoes':votacoes,
                                                 })

@login_required
def vervotacao(request, id):
    pegaVotacao = Votacao.objects.get(id=id)
    pegaCandidato1 = Candidatos.objects.get(id=pegaVotacao.candidato1_id)
    pegaCandidato2 = Candidatos.objects.get(id=pegaVotacao.candidato2_id)
    return render(request, 'site/votacao.html', {'pegaVotacao':pegaVotacao,
                                                 'pegaCandidato1':pegaCandidato1,
                                                 'pegaCandidato2':pegaCandidato2,
                                                 })

@login_required
def relatorio(request, id):
    pegaVotacao = Votacao.objects.get(id=id)
    pegaCandidato1 = Candidatos.objects.get(id=pegaVotacao.candidato1_id)
    pegaCandidato2 = Candidatos.objects.get(id=pegaVotacao.candidato2_id)
    pegoVotoCandidato1 = Voto.objects.filter(voto=pegaCandidato1, votacao=pegaVotacao).count()
    pegoVotoCandidato2 = Voto.objects.filter(voto=pegaCandidato2, votacao=pegaVotacao).count()

    return render(request, 'site/resultado.html', {'pegoVotoCandidato1':pegoVotoCandidato1,
                                                   'pegoVotoCandidato2':pegoVotoCandidato2,
                                                   'pegaVotacao': pegaVotacao,
                                                   })

@login_required
def sair(request):
    logout(request)
    return redirect(inicial)

@login_required
def perfil(request):
    verificaExiste = UsuarioPerfil.objects.filter(user_id=request.user.id)
    if verificaExiste.exists():
        pessoa = get_object_or_404(UsuarioPerfil, user_id=request.user.id)
        form = UsuarioPerfilForm(request.POST or None, instance=pessoa)
        if form.is_valid():
            form.save()
            messages.success(request, 'Obrigado por atualizar seu perfil!')
            return redirect(inicial)
    else:
        form = UsuarioPerfilForm(request.POST or None)
        if form.is_valid():
            Formulario = form.save(commit=False)
            Formulario.user_id = request.user.id
            Formulario.save()
            messages.success(request, 'Agora você está pronto para fazer uma votação. :)')
            return redirect(inicial)

    return render(request, 'site/perfil.html', {'form': form})

def cadastro(request):
    if request.method == 'POST':
        form = RegistroUsuario(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(inicial)
    else:
        form = RegistroUsuario()
    return render(request, 'site/cadastro.html', {'form': form})

@login_required
def votar(request, id, candidato):
    try:
        Voto.objects.get(user=request.user, votacao_id=id)
        messages.error(request, 'Você já votou nesta votação!')
        return redirect(vervotacao, id=id)
    except:
        pass

    try:
        UsuarioPerfil.objects.get(user=request.user)
    except:
        messages.error(request, 'Complete seu perfil!')
        return redirect(perfil)
    pegaVotacao = Votacao.objects.get(id=id)
    if pegaVotacao.status == 'Fechada':
        messages.error(request, 'Votação fechada!')
        return redirect(inicial)
    Voto.objects.create(user=request.user, votacao_id=id, voto_id=candidato)
    messages.success(request, 'Voto computado com sucesso!')
    return redirect(vervotacao, id=id)

