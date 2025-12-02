from django.urls import path

from .views import (
    SolicitarCodigoEsqueceuSenhaPostView,
    ValidarCodigoEmailPostView,
    RedefinirSenhaPostView,
)

app_name = 'conta'

urlpatterns = [
    path('esqueci_minha_senha/', SolicitarCodigoEsqueceuSenhaPostView.as_view(), name='esqueci-senha'),
    path('validar_codigo/', ValidarCodigoEmailPostView.as_view(), name='validar-codigo'),
    path('redefinir_senha/', RedefinirSenhaPostView.as_view(), name='redefinir-senha'),
]
