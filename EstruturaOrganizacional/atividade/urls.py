from django.urls import path

from EstruturaOrganizacional.atividade.views import (
    AtividadeListaView,
    AtividadeCriarView,
    AtividadeEditarView,
    AtividadeDeletarView,
)

app_name = 'atividade'

urlpatterns = [
    path('', AtividadeListaView.as_view(), name='atividade-lista'),
    path('criar/', AtividadeCriarView.as_view(), name='atividade-criar'),
    path('<int:pk>/editar/', AtividadeEditarView.as_view(), name='atividade-editar'),
    path('<int:pk>/deletar/', AtividadeDeletarView.as_view(), name='atividade-deletar'),
]
