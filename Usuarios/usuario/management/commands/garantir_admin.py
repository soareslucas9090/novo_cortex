from datetime import date

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Garante que exista um usuário admin padrão com CPF 12345678901'

    CPF_ADMIN = '12345678901'
    SENHA_ADMIN = 'Senh@123'
    NOME_ADMIN = 'Administrador Padrão'

    def handle(self, *args, **options):
        # Importa aqui para evitar problemas de importação circular
        from Usuarios.usuario.models import Usuario
        from EstruturaOrganizacional.campus.models import Campus

        self.stdout.write('Verificando usuário admin padrão...')

        # Verifica se existe um usuário com o CPF padrão e senha correta
        usuario_existe = False
        try:
            usuario = Usuario.objects.get(cpf=self.CPF_ADMIN)
            if usuario.check_password(self.SENHA_ADMIN):
                usuario_existe = True
                self.stdout.write(
                    self.style.SUCCESS(f'Usuário admin padrão já existe e senha está correta.')
                )
        except Usuario.DoesNotExist:
            pass
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Erro ao verificar usuário: {e}')
            )

        if not usuario_existe:
            # Remove todos os usuários com o CPF padrão
            deleted_count, _ = Usuario.objects.filter(cpf=self.CPF_ADMIN).delete()
            if deleted_count > 0:
                self.stdout.write(
                    self.style.WARNING(f'Removidos {deleted_count} usuário(s) com CPF {self.CPF_ADMIN}')
                )

            # Garante que existe um campus para vincular o usuário
            campus = Campus.objects.first()
            if not campus:
                campus = Campus.objects.create(
                    nome='Campus Padrão',
                    cnpj='00000000000000',
                    is_active=True,
                )
                self.stdout.write(
                    self.style.WARNING('Campus padrão criado para vincular o usuário admin.')
                )

            # Cria o usuário admin
            usuario = Usuario.objects.create_superuser(
                cpf=self.CPF_ADMIN,
                nome=self.NOME_ADMIN,
                password=self.SENHA_ADMIN,
                campus=campus,
                data_nascimento=date(2000, 1, 1),
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f'Usuário admin criado com sucesso!\n'
                    f'  CPF: {self.CPF_ADMIN}\n'
                    f'  Senha: {self.SENHA_ADMIN}\n'
                    f'  Nome: {self.NOME_ADMIN}'
                )
            )
