from django.urls import path

from Usuarios.usuario.views import UsuarioListaView

app_name = 'usuarios'

urlpatterns = [
    path('', UsuarioListaView.as_view(), name='lista'),
]
