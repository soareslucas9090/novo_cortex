from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


@extend_schema(tags=["Auth"])
class ObterParTokenViewDOC(TokenObtainPairView):
    pass


@extend_schema(tags=["Auth"])
class AtualizarTokenViewDOC(TokenRefreshView):
    pass


@extend_schema(tags=["Auth"])
class VerificarTokenViewDOC(TokenVerifyView):
    pass