from django.urls import path

from Perfis.terceirizado.views import (
    TerceirizadoListaView,
    TerceirizadoDetalheView,
    TerceirizadoCriarView,
    TerceirizadoEditarView,
    TerceirizadoDeletarView,
)

app_name = 'terceirizado'

urlpatterns = [
    path('', TerceirizadoListaView.as_view(), name='lista'),
    path('criar/', TerceirizadoCriarView.as_view(), name='criar'),
    path('<int:pk>/', TerceirizadoDetalheView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', TerceirizadoEditarView.as_view(), name='editar'),
    path('<int:pk>/deletar/', TerceirizadoDeletarView.as_view(), name='deletar'),
]
