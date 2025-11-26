from django.urls import path

from .views import (
    CriarContaPostView,
    ConfirmarCodigoCriarContaPostView,
    ConfirmarSenhaContaPostView,
    SolicitarCodigoEsqueceuSenhaPostView
)

app_name = 'account'

urlpatterns = [
    path('create/', CriarContaPostView.as_view(), name='create-account'),
    path('create/confirm-code/', ConfirmarCodigoCriarContaPostView.as_view(), name='create-account-confirm-code'),
    path('create/confirm-password/', ConfirmarSenhaContaPostView.as_view(), name='create-account-confirm-password'),
    path('forgot_password/', SolicitarCodigoEsqueceuSenhaPostView.as_view(), name='forgot-password'),
]
