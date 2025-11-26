from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Users.users'
    verbose_name = 'Usuários'
    
    def ready(self):
        import Users.users.signals
