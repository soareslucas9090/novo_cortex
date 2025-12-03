from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from EstruturaOrganizacional.cargo.business import CargoBusiness


class Cargo(ModelBusinessMixin, BasicModel):
    """
    Representa um cargo na instituição.
    
    Relacionamentos:
    - Cargo (1) → (*) Usuario
    """
    descricao = models.CharField(
        'Descrição',
        max_length=255,
        unique=True,
    )

    business_class = CargoBusiness
    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'cargos'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao
