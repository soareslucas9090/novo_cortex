from django.urls import path

from EstruturaOrganizacional.cargo.views import (
    CargoListaView,
    CargoCriarView,
    CargoEditarView,
    CargoDeletarView,
)

app_name = 'cargo'

urlpatterns = [
    path('', CargoListaView.as_view(), name='cargo-lista'),
    path('criar/', CargoCriarView.as_view(), name='cargo-criar'),
    path('<int:pk>/editar/', CargoEditarView.as_view(), name='cargo-editar'),
    path('<int:pk>/deletar/', CargoDeletarView.as_view(), name='cargo-deletar'),
]
