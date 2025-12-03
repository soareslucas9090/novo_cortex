from django.db import models

from AppCore.basics.models.models import BasicModel
from AppCore.core.business.business_mixin import ModelBusinessMixin

from EstruturaOrganizacional.atividade.business import AtividadeBusiness
from EstruturaOrganizacional.setor.models import Setor


class Atividade(ModelBusinessMixin, BasicModel):
    """
    Representa uma atividade dentro de um setor.
    
    Relacionamentos:
    - Setor (1) → (*) Atividade
    - Atividade (1) → (*) Funcao
    """
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='atividades',
        verbose_name='Setor',
    )
    descricao = models.TextField(
        'Descrição',
    )
    eh_gratificada = models.BooleanField(
        'É gratificada',
        default=False,
        help_text='Indica se a atividade é considerada para gratificação.',
    )
    
    business_class = AtividadeBusiness

    class Meta:
        db_table = 'atividades'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['setor', 'descricao']

    def __str__(self):
        return f'{self.setor.nome} - {self.descricao[:50]}'
