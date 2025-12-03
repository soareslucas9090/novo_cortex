from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from EstruturaOrganizacional.curso.business import CursoBusiness


class Curso(ModelBusinessMixin, BasicModel):
    """
    Representa um curso (para estagiários).
    
    Relacionamentos:
    - Curso (1) → (*) Estagiario
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    descricao = models.TextField(
        'Descrição',
        blank=True,
        null=True,
    )

    business_class = CursoBusiness
    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']

    def __str__(self):
        return self.nome
