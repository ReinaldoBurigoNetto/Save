from django.contrib import admin
from .models import UsuarioPerfil, Candidatos, Votacao, Voto
# Register your models here.

admin.site.register(UsuarioPerfil)
admin.site.register(Candidatos)
admin.site.register(Votacao)
admin.site.register(Voto)
