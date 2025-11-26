from django.urls import path
from .views import (
    ObterParTokenViewDOC,
    AtualizarTokenViewDOC,
    VerificarTokenViewDOC,
)

app_name = 'token-jwt'

urlpatterns = [
    path('', ObterParTokenViewDOC.as_view(), name='token-obtain-pair'),
    path('refresh/', AtualizarTokenViewDOC.as_view(), name='token-refresh'),
    path('verify/', VerificarTokenViewDOC.as_view(), name='token-verify'),
]
