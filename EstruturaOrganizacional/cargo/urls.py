from django.urls import path

from EstruturaOrganizacional.cargo.views import (
    CargoListaView,
    CargoCriarView,
)

app_name = 'cargo'

urlpatterns = [
    path('', CargoListaView.as_view(), name='cargo-lista'),
    path('criar/', CargoCriarView.as_view(), name='cargo-criar'),
]
