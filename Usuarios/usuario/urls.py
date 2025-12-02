from django.urls import path

from Usuarios.usuario.views import UsuarioListaView, UsuarioRetrieveView

app_name = 'usuarios'

urlpatterns = [
    path('', UsuarioListaView.as_view(), name='lista'),
    path('<int:pk>/', UsuarioRetrieveView.as_view(), name='detalhe'),
]
