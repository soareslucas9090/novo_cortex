from django.urls import path, include

app_name = 'estrutura-organizacional'

urlpatterns = [
    path('campus/', include('EstruturaOrganizacional.campus.urls')),
    path('cargos/', include('EstruturaOrganizacional.cargo.urls')),
    path('setores/', include('EstruturaOrganizacional.setor.urls')),
    path('atividades/', include('EstruturaOrganizacional.atividade.urls')),
    path('funcoes/', include('EstruturaOrganizacional.funcao.urls')),
    path('empresas/', include('EstruturaOrganizacional.empresa.urls')),
    path('cursos/', include('EstruturaOrganizacional.curso.urls')),
]
