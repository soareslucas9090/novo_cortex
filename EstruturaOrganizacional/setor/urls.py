from django.urls import path

from EstruturaOrganizacional.setor.views import (
    SetorListaView,
    SetorCriarView,
)

app_name = 'setor'

urlpatterns = [
    path('', SetorListaView.as_view(), name='setor-lista'),
    path('criar/', SetorCriarView.as_view(), name='setor-criar'),
]
