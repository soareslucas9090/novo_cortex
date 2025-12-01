from django.urls import path

from .views import SolicitarCodigoEsqueceuSenhaPostView

app_name = 'conta'

urlpatterns = [
    path('esqueci_minha_senha/', SolicitarCodigoEsqueceuSenhaPostView.as_view(), name='esqueci-senha'),
]
