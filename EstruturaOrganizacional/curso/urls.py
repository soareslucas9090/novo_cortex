from django.urls import path

from EstruturaOrganizacional.curso.views import (
    CursoListaView,
    CursoCriarView,
    CursoEditarView,
    CursoDeletarView,
)

app_name = 'curso'

urlpatterns = [
    path('', CursoListaView.as_view(), name='curso-lista'),
    path('criar/', CursoCriarView.as_view(), name='curso-criar'),
    path('<int:pk>/editar/', CursoEditarView.as_view(), name='curso-editar'),
    path('<int:pk>/deletar/', CursoDeletarView.as_view(), name='curso-deletar'),
]
