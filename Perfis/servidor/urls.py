from django.urls import path

from Perfis.servidor.views import (
    ServidorListaView,
    ServidorDetalheView,
    ServidorCriarView,
    ServidorEditarView,
    ServidorDeletarView,
)

app_name = 'servidor'

urlpatterns = [
    path('', ServidorListaView.as_view(), name='lista'),
    path('criar/', ServidorCriarView.as_view(), name='criar'),
    path('<int:pk>/', ServidorDetalheView.as_view(), name='detalhe'),
    path('<int:pk>/editar/', ServidorEditarView.as_view(), name='editar'),
    path('<int:pk>/deletar/', ServidorDeletarView.as_view(), name='deletar'),
]
