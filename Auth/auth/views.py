from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import TokenPersonalizadoSerializer


@extend_schema(tags=["Auth"])
class ObterParTokenViewDOC(TokenObtainPairView):
    serializer_class = TokenPersonalizadoSerializer


@extend_schema(tags=["Auth"])
class AtualizarTokenViewDOC(TokenRefreshView):
    pass


@extend_schema(tags=["Auth"])
class VerificarTokenViewDOC(TokenVerifyView):
    pass