from django.urls import path

from EstruturaOrganizacional.curso.views import (
    CursoListaView,
    CursoCriarView,
    CursoEditarView,
)

app_name = 'curso'

urlpatterns = [
    path('', CursoListaView.as_view(), name='curso-lista'),
    path('criar/', CursoCriarView.as_view(), name='curso-criar'),
    path('<int:pk>/editar/', CursoEditarView.as_view(), name='curso-editar'),
]
