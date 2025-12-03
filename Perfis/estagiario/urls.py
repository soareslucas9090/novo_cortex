from django.urls import path

from Perfis.estagiario.views import (
    EstagiarioListaView,
    EstagiarioDetalheView,
    EstagiarioCriarView,
    EstagiarioEditarView,
    EstagiarioDeletarView,
)

app_name = 'estagiario'

urlpatterns = [
    path('', EstagiarioListaView.as_view(), name='lista'),
    path('criar/', EstagiarioCriarView.as_view(), name='criar'),
    path('<int:pk>/', EstagiarioDetalheView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', EstagiarioEditarView.as_view(), name='editar'),
    path('<int:pk>/deletar/', EstagiarioDeletarView.as_view(), name='deletar'),
]
