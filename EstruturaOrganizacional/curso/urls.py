from django.urls import path

from EstruturaOrganizacional.curso.views import (
    CursoListaView,
    CursoCriarView,
)

app_name = 'curso'

urlpatterns = [
    path('', CursoListaView.as_view(), name='curso-lista'),
    path('criar/', CursoCriarView.as_view(), name='curso-criar'),
]
