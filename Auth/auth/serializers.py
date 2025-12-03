from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from AppCore.common.util.util import formatar_cpf


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para login via CPF.
    
    Além dos tokens (access e refresh), retorna:
    - Dados básicos do usuário (id, nome, cpf)
    - Campus
    - Tipo(s) de perfil
    - Setores vinculados com função e atividades
    - Permissões administrativas
    """
    username_field = 'cpf'

    def validate(self, attrs):
        # Chama o validate pai para obter os tokens
        data = super().validate(attrs)
        
        # Adiciona dados do usuário na resposta
        usuario = self.user
        
        # Dados básicos
        data['usuario'] = {
            'id': usuario.id,
            'nome': usuario.nome,
            'cpf': usuario.cpf,
            'cpf_formatado': formatar_cpf(usuario.cpf),
            'data_nascimento': usuario.data_nascimento,
            'data_ingresso': usuario.data_ingresso,
            'ativo': usuario.ativo,
            'is_admin': usuario.is_admin,
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser,
        }
        
        # Campus
        data['campus'] = {
            'id': usuario.campus.id,
            'nome': usuario.campus.nome,
        }
        
        # Tipo(s) de perfil
        data['perfis'] = self._obter_perfis(usuario)
        
        # Setores vinculados (ativos)
        data['setores'] = self._obter_setores(usuario)
        
        # Permissões resumidas
        data['permissoes'] = {
            'is_admin': usuario.is_admin,
            'is_staff': usuario.is_staff,
            'is_superuser': usuario.is_superuser,
            'e_responsavel_setor': self._verifica_responsavel(usuario),
            'e_monitor': self._verifica_monitor(usuario),
        }
        
        return data

    def _obter_perfis(self, usuario):
        """Retorna os perfis do usuário com dados resumidos."""
        perfis = []
        
        # Servidor
        try:
            if hasattr(usuario, 'servidor') and usuario.servidor:
                servidor = usuario.servidor
                perfis.append({
                    'tipo': 'Servidor',
                    'dados': {
                        'tipo_servidor': servidor.tipo_servidor,
                        'jornada_trabalho': servidor.get_jornada_trabalho_display(),
                        'classe': servidor.classe,
                        'padrao': servidor.padrao,
                    }
                })
        except:
            pass
        
        # Aluno
        try:
            if hasattr(usuario, 'aluno') and usuario.aluno:
                aluno = usuario.aluno
                perfis.append({
                    'tipo': 'Aluno',
                    'dados': {
                        'ira': str(aluno.ira),
                        'turno': aluno.get_turno_display(),
                        'forma_ingresso': aluno.get_forma_ingresso_display(),
                        'aluno_especial': aluno.aluno_especial,
                        'is_formado': aluno.is_formado,
                    }
                })
        except:
            pass
        
        # Terceirizado
        try:
            if hasattr(usuario, 'terceirizado') and usuario.terceirizado:
                terceirizado = usuario.terceirizado
                perfis.append({
                    'tipo': 'Terceirizado',
                    'dados': {
                        'empresa': {
                            'id': terceirizado.empresa.id,
                            'nome': terceirizado.empresa.nome,
                        },
                        'data_inicio_contrato': terceirizado.data_inicio_contrato,
                        'data_fim_contrato': terceirizado.data_fim_contrato,
                    }
                })
        except:
            pass
        
        # Estagiário
        try:
            if hasattr(usuario, 'estagiario') and usuario.estagiario:
                estagiario = usuario.estagiario
                perfis.append({
                    'tipo': 'Estagiário',
                    'dados': {
                        'empresa': {
                            'id': estagiario.empresa.id,
                            'nome': estagiario.empresa.nome,
                        },
                        'curso': {
                            'id': estagiario.curso.id,
                            'nome': estagiario.curso.nome,
                        },
                        'carga_horaria': estagiario.carga_horaria,
                        'data_inicio_estagio': estagiario.data_inicio_estagio,
                        'data_fim_estagio': estagiario.data_fim_estagio,
                    }
                })
        except:
            pass
        
        return perfis if perfis else [{'tipo': 'Sem perfil', 'dados': None}]

    def _obter_setores(self, usuario):
        """Retorna os setores ativos do usuário com atividades e funções."""
        setores = []
        
        usuario_setores = usuario.usuario_setores.filter(
            data_saida__isnull=True
        ).select_related('setor', 'campus')
        
        for us in usuario_setores:
            setor_data = {
                'id': us.id,
                'setor': {
                    'id': us.setor.id,
                    'nome': us.setor.nome,
                },
                'campus': {
                    'id': us.campus.id,
                    'nome': us.campus.nome,
                },
                'e_responsavel': us.e_responsavel,
                'monitor': us.monitor,
                'data_entrada': us.data_entrada,
                'atividades': self._obter_atividades_setor(us.setor),
            }
            setores.append(setor_data)
        
        return setores

    def _obter_atividades_setor(self, setor):
        """Retorna as atividades e funções de um setor."""
        atividades = []
        
        for atividade in setor.atividades.all():
            atividade_data = {
                'id': atividade.id,
                'descricao': atividade.descricao[:100] if len(atividade.descricao) > 100 else atividade.descricao,
                'funcoes': [
                    {
                        'id': funcao.id,
                        'descricao': funcao.descricao[:100] if len(funcao.descricao) > 100 else funcao.descricao,
                    }
                    for funcao in atividade.funcoes.all()
                ]
            }
            atividades.append(atividade_data)
        
        return atividades

    def _verifica_responsavel(self, usuario):
        """Verifica se o usuário é responsável por algum setor."""
        return usuario.usuario_setores.filter(
            e_responsavel=True,
            data_saida__isnull=True
        ).exists()

    def _verifica_monitor(self, usuario):
        """Verifica se o usuário é monitor em algum setor."""
        return usuario.usuario_setores.filter(
            monitor=True,
            data_saida__isnull=True
        ).exists()


class LoginResponseSerializer(serializers.Serializer):
    """
    Serializer para documentação da resposta de login.
    
    Usado apenas para documentação no Swagger/OpenAPI.
    """
    access = serializers.CharField(help_text='Token de acesso JWT')
    refresh = serializers.CharField(help_text='Token de refresh JWT')
    usuario = serializers.DictField(help_text='Dados do usuário autenticado')
    campus = serializers.DictField(help_text='Campus do usuário')
    perfis = serializers.ListField(help_text='Lista de perfis do usuário')
    setores = serializers.ListField(help_text='Setores vinculados ao usuário')
    permissoes = serializers.DictField(help_text='Permissões do usuário')


class LoginInputSerializer(serializers.Serializer):
    """
    Serializer para documentação do input de login.
    
    Usado apenas para documentação no Swagger/OpenAPI.
    """
    cpf = serializers.CharField(
        help_text='CPF do usuário (apenas números, 11 dígitos)',
        max_length=11,
        min_length=11,
    )
    password = serializers.CharField(
        help_text='Senha do usuário',
        write_only=True,
    )
