from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def pegaNome(self):
    return self.first_name + ' ' + self.last_name + ' - ' + self.username

User.add_to_class("__str__", pegaNome)

class UsuarioPerfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14)
    biografia = models.TextField()

    class Meta:
        verbose_name_plural = '1 - Perfis dos Usuários'
        verbose_name = '1 - Perfis dos Usuários'

    def __str__(self):
        return str(self.user)

class Candidatos(models.Model):
    nome = models.CharField(max_length=255)
    biografia = models.TextField()
    imagem = models.ImageField(upload_to='fotoscandidatos')

    class Meta:
        verbose_name_plural = '2 - Candidatos'
        verbose_name = '2 - Candidatos'

    def __str__(self):
        return str(self.nome)

class Votacao(models.Model):
    ABERTA = 'Aberta'
    FECHADA = 'Fechada'
    VOTACAO_CHOICES= (
        (ABERTA, 'Aberta'),
        (FECHADA, 'Fechada'),
    )

    nome = models.CharField(max_length=255, default='')
    candidato1 = models.ForeignKey(Candidatos, on_delete=models.CASCADE, related_name='candidato1')
    candidato2 = models.ForeignKey(Candidatos, on_delete=models.CASCADE, related_name='candidato2')
    status = models.CharField(max_length=15, choices=VOTACAO_CHOICES, default=ABERTA)

    class Meta:
        verbose_name_plural = '3 - Votações'
        verbose_name = '3 - Votações'

    def __str__(self):
        return str(self.nome) + ' - ' + str(self.candidato1) + ' x ' + str(self.candidato2)

class Voto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    votacao = models.ForeignKey(Votacao, on_delete=models.CASCADE)
    voto = models.ForeignKey(Candidatos, on_delete=models.CASCADE, default='')

    class Meta:
        verbose_name_plural = '4 - Votos'
        verbose_name = '4 - Votos'

    def __str__(self):
        return str(self.user) + ' - ' + str(self.votacao)