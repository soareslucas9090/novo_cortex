from django.urls import path

from Perfis.aluno.views import (
    AlunoListaView,
    AlunoDetalheView,
    AlunoCriarView,
    AlunoEditarView,
    AlunoDeletarView,
)

app_name = 'aluno'

urlpatterns = [
    path('', AlunoListaView.as_view(), name='lista'),
    path('criar/', AlunoCriarView.as_view(), name='criar'),
    path('<int:pk>/', AlunoDetalheView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', AlunoEditarView.as_view(), name='editar'),
    path('<int:pk>/deletar/', AlunoDeletarView.as_view(), name='deletar'),
]
