from django.urls import path

from EstruturaOrganizacional.empresa.views import (
    EmpresaListaView,
    EmpresaCriarView,
)

app_name = 'empresa'

urlpatterns = [
    path('', EmpresaListaView.as_view(), name='empresa-lista'),
    path('criar/', EmpresaCriarView.as_view(), name='empresa-criar'),
]
