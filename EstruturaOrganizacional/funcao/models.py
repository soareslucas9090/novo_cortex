from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager

from EstruturaOrganizacional.atividade.models import Atividade


class Funcao(BasicModel):
    """
    Representa uma função dentro de uma atividade.
    
    Relacionamentos:
    - Atividade (1) → (*) Funcao
    """
    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.PROTECT,
        related_name='funcoes',
        verbose_name='Atividade',
    )
    descricao = models.TextField(
        'Descrição',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'funcoes'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['atividade', 'descricao']

    def __str__(self):
        return f'{self.atividade.setor.nome} - {self.descricao[:50]}'
