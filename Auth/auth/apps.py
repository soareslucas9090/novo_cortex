from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Auth.auth'
    label = 'auth_app'
    verbose_name = 'Autenticação'
