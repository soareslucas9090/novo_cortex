from django.urls import path, include

app_name = 'perfis'

urlpatterns = [
    path('alunos/', include('Perfis.aluno.urls')),
    path('estagiarios/', include('Perfis.estagiario.urls')),
    path('servidores/', include('Perfis.servidor.urls')),
    path('terceirizados/', include('Perfis.terceirizado.urls')),
]
