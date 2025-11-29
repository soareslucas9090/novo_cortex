from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager

from EstruturaOrganizacional.setor.models import Setor


class Atividade(BasicModel):
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

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'atividades'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['setor', 'descricao']

    def __str__(self):
        return f'{self.setor.nome} - {self.descricao[:50]}'
