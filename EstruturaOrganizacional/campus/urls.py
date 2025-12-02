from django.urls import path

from EstruturaOrganizacional.campus.views import (
    CampusListaView,
    CampusCriarView,
    CampusEditarView,
)

app_name = 'campus'

urlpatterns = [
    path('', CampusListaView.as_view(), name='campus-lista'),
    path('criar/', CampusCriarView.as_view(), name='campus-criar'),
    path('<int:pk>/editar/', CampusEditarView.as_view(), name='campus-editar'),
]
