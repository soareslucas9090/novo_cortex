from django.urls import path
from .views import (
    TokenObtainPairViewDOC,
    TokenRefreshViewDOC,
    TokenVerifyViewDOC,
)

app_name = 'token-jwt'

urlpatterns = [
    path('', TokenObtainPairViewDOC.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshViewDOC.as_view(), name='token-refresh'),
    path('verify/', TokenVerifyViewDOC.as_view(), name='token-verify'),
]
