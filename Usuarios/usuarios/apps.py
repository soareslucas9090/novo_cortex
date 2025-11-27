from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios.usuarios'
    verbose_name = 'Usuários'
    
    def ready(self):
        import Usuarios.usuarios.signals
