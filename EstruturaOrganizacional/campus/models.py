from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from EstruturaOrganizacional.campus.business import CampusBusiness


class Campus(ModelBusinessMixin, BasicModel):
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
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    business_class = CampusBusiness
    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'campus'
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'
        ordering = ['nome']

    def __str__(self):
        return self.nome
