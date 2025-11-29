from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager

from EstruturaOrganizacional.atividade.models import Atividade


class UsuarioSetor(BasicModel):
    """
    Tabela associativa entre Usuario e Setor.
    
    Representa a associação de um usuário a um setor, com informações
    sobre responsabilidade, monitor e datas.
    
    Relacionamentos:
    - Usuario (*) ↔ (*) Setor
    - UsuarioSetor → Campus (referência ao campus do setor)
    """
    usuario = models.ForeignKey(
        "usuario.Usuario",
        on_delete=models.CASCADE,
        related_name='usuario_setores',
        verbose_name='Usuário',
    )
    setor = models.ForeignKey(
        "setor.Setor",
        on_delete=models.PROTECT,
        related_name='usuario_setores',
        verbose_name='Setor',
    )
    campus = models.ForeignKey(
        "campus.Campus",
        on_delete=models.PROTECT,
        related_name='usuario_setores',
        verbose_name='Campus',
    )
    e_responsavel = models.BooleanField(
        'É Responsável',
        default=False,
    )
    monitor = models.BooleanField(
        'Monitor',
        default=False,
    )
    data_entrada = models.DateField(
        'Data de Entrada',
        default=timezone.now(),
    )
    data_saida = models.DateField(
        'Data de Saída',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'usuario_setor'
        verbose_name = 'Usuário-Setor'
        verbose_name_plural = 'Usuários-Setores'
        ordering = ['usuario', 'setor']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'setor'],
                name='unique_usuario_setor'
            )
        ]

    def __str__(self):
        return f'{self.usuario.nome} - {self.setor.nome}'
