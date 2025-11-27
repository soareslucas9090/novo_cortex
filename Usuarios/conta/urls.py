from django.urls import path

from .views import (
    CriarContaPostView,
    ConfirmarCodigoCriarContaPostView,
    ConfirmarSenhaContaPostView,
    SolicitarCodigoEsqueceuSenhaPostView
)

app_name = 'conta'

urlpatterns = [
    path('create/', CriarContaPostView.as_view(), name='create-conta'),
    path('create/confirm-code/', ConfirmarCodigoCriarContaPostView.as_view(), name='create-conta-confirm-code'),
    path('create/confirm-password/', ConfirmarSenhaContaPostView.as_view(), name='create-conta-confirm-password'),
    path('forgot_password/', SolicitarCodigoEsqueceuSenhaPostView.as_view(), name='forgot-password'),
]
