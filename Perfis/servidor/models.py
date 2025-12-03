from django.db import models

from AppCore.basics.models.models import BasicModel, BaseManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from . import choices
from .business import ServidorBusiness


class Servidor(ModelBusinessMixin, BasicModel):
    """
    Representa um servidor da instituição.
    
    Herança via OneToOne:
    - Usuario ← Servidor
    
    Campos do DER:
    - data_posse
    - jornada_trabalho (INTEGER)
    - padrao (VARCHAR)
    - classe (VARCHAR)
    - tipo_servidor (VARCHAR)
    """
    business_class = ServidorBusiness
    
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='servidor',
        verbose_name='Usuário',
        primary_key=True,
    )
    data_posse = models.DateField(
        'Data de Posse',
    )
    jornada_trabalho = models.IntegerField(
        'Jornada de Trabalho',
        choices=choices.JORNADA_OPCOES,
        default=choices.JORNADA_40,
        help_text='Horas semanais (0 = Dedicação Exclusiva)',
    )
    padrao = models.CharField(
        'Padrão',
        max_length=50,
    )
    classe = models.CharField(
        'Classe',
        max_length=50,
    )
    tipo_servidor = models.CharField(
        'Tipo de Servidor',
        max_length=100,
        help_text='Ex: Professor, Técnico Administrativo, etc.',
    )

    class Meta:
        db_table = 'servidores'
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.tipo_servidor}'
