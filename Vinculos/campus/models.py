from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager


class Campus(BasicModel):
    """
    Representa um campus da instituição.
    
    Relacionamentos:
    - Campus (1) → (*) Usuario
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    cnpj = models.CharField(
        'CNPJ',
        max_length=14,
        unique=True,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'campus'
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    

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
