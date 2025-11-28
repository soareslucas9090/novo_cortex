from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager


class Cargo(BasicModel):
    """
    Representa um cargo na instituição.
    
    Entidade simples sem relacionamentos diretos no DER.
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'cargos'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
