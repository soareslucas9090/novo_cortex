from django.urls import path

from EstruturaOrganizacional.empresa.views import (
    EmpresaListaView,
    EmpresaCriarView,
    EmpresaEditarView,
    EmpresaDeletarView,
)

app_name = 'empresa'

urlpatterns = [
    path('', EmpresaListaView.as_view(), name='empresa-lista'),
    path('criar/', EmpresaCriarView.as_view(), name='empresa-criar'),
    path('<int:pk>/editar/', EmpresaEditarView.as_view(), name='empresa-editar'),
    path('<int:pk>/deletar/', EmpresaDeletarView.as_view(), name='empresa-deletar'),
]
