from django.apps import AppConfig


class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Usuarios.usuario'
    label = 'usuarios'
    verbose_name = 'Usuário'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(garantir_admin_padrao, sender=self)


def garantir_admin_padrao(sender, **kwargs):
    """
    Garante que exista um usuário admin padrão após cada migrate.
    
    CPF: 12345678901
    Senha: Senh@123
    """
    from datetime import date
    from django.db import connection
    
    # Verifica se as tabelas necessárias existem
    tables = connection.introspection.table_names()
    if 'usuarios' not in tables or 'campus' not in tables:
        return
    
    from Usuarios.usuario.models import Usuario
    from EstruturaOrganizacional.campus.models import Campus

    CPF_ADMIN = '12345678901'
    SENHA_ADMIN = 'Senh@123'
    NOME_ADMIN = 'Administrador Padrão'

    # Verifica se existe um usuário com o CPF padrão e senha correta
    usuario_existe = False
    try:
        usuario = Usuario.objects.get(cpf=CPF_ADMIN)
        if usuario.check_password(SENHA_ADMIN):
            usuario_existe = True
    except Usuario.DoesNotExist:
        pass
    except Exception:
        pass

    if not usuario_existe:
        # Remove todos os usuários com o CPF padrão
        Usuario.objects.filter(cpf=CPF_ADMIN).delete()

        # Garante que existe um campus para vincular o usuário
        campus = Campus.objects.first()
        if not campus:
            campus = Campus.objects.create(
                nome='Campus Padrão',
                cnpj='00000000000000',
                ativo=True,
            )

        # Cria o usuário admin
        Usuario.objects.create_superuser(
            cpf=CPF_ADMIN,
            nome=NOME_ADMIN,
            password=SENHA_ADMIN,
            campus=campus,
            data_nascimento=date(2000, 1, 1),
        )
        print(f'\n[INFO] Usuário admin padrão criado: CPF={CPF_ADMIN}, Senha={SENHA_ADMIN}\n')
