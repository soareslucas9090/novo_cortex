from django.urls import path

from .views import (
    CreateAccountPostView,
    CreateAccountConfirmCodePostView,
    ConfirmPasswordAccountPostView,
    RequestForgotPasswordCodePostView
)

app_name = 'account'

urlpatterns = [
    path('create/', CreateAccountPostView.as_view(), name='create-account'),
    path('create/confirm-code/', CreateAccountConfirmCodePostView.as_view(), name='create-account-confirm-code'),
    path('create/confirm-password/', ConfirmPasswordAccountPostView.as_view(), name='create-account-confirm-password'),
    path('forgot_password/', RequestForgotPasswordCodePostView.as_view(), name='forgot-password'),
]
