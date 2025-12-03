from django.db import models

from AppCore.basics.models.models import BasicModel, BaseManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from .business import TerceirizadoBusiness


class Terceirizado(ModelBusinessMixin, BasicModel):
    """
    Representa um funcionário terceirizado.
    
    Herança via OneToOne:
    - Usuario ← Terceirizado
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    """
    business_class = TerceirizadoBusiness
    
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='terceirizado',
        verbose_name='Usuário',
        primary_key=True,
    )
    empresa = models.ForeignKey(
        "empresa.Empresa",
        on_delete=models.PROTECT,
        related_name='terceirizados',
        verbose_name='Empresa',
    )
    data_inicio_contrato = models.DateField(
        'Data de Início do Contrato',
    )
    data_fim_contrato = models.DateField(
        'Data de Fim do Contrato',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'terceirizados'
        verbose_name = 'Terceirizado'
        verbose_name_plural = 'Terceirizados'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.empresa.nome}'
