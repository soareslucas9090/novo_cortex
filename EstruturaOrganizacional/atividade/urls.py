from django.urls import path

from EstruturaOrganizacional.atividade.views import (
    AtividadeListaView,
    AtividadeCriarView,
)

app_name = 'atividade'

urlpatterns = [
    path('', AtividadeListaView.as_view(), name='atividade-lista'),
    path('criar/', AtividadeCriarView.as_view(), name='atividade-criar'),
]
