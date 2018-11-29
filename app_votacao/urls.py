from django.urls import path
from .views import inicial, vervotacao, votar, relatorio, perfil, cadastro, sair
#Sistema de Login
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', inicial, name='votacao_inicial'),
    path('votacao/<int:id>', vervotacao, name='votacao_vervotacao'),
    path('votacao/<int:id>/votar/<int:candidato>/', votar, name='votacao_votar'),
    path('votacao/<int:id>/relatorio', relatorio, name='votacao_relatorio'),
    path('site/perfil', perfil, name='site_perfil'),
    path('site/login', auth_views.LoginView.as_view(), name='site_login'),
    path('site/cadastro', cadastro, name='site_cadastro'),
    path('site/sair', sair, name='site_sair'),
]