from django.urls import path

from EstruturaOrganizacional.funcao.views import (
    FuncaoListaView,
    FuncaoCriarView,
    FuncaoEditarView,
)

app_name = 'funcao'

urlpatterns = [
    path('', FuncaoListaView.as_view(), name='funcao-lista'),
    path('criar/', FuncaoCriarView.as_view(), name='funcao-criar'),
    path('<int:pk>/editar/', FuncaoEditarView.as_view(), name='funcao-editar'),
]
