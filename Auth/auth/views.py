from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import CustomTokenObtainPairSerializer


@extend_schema(tags=["Auth"])
class TokenObtainPairViewDOC(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=["Auth"])
class TokenRefreshViewDOC(TokenRefreshView):
    pass


@extend_schema(tags=["Auth"])
class TokenVerifyViewDOC(TokenVerifyView):
    pass