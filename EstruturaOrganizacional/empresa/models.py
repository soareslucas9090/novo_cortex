from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.business.business_mixin import ModelBusinessMixin

from EstruturaOrganizacional.empresa.business import EmpresaBusiness


class Empresa(ModelBusinessMixin, BasicModel):
    """
    Representa uma empresa (terceirizada ou instituição externa).
    
    Unifica Empresa e InstituicaoExterna do DER anterior.
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    - Empresa (1) → (*) Estagiario
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

    business_class = EmpresaBusiness
    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa/Instituição'
        verbose_name_plural = 'Empresas/Instituições'
        ordering = ['nome']

    def __str__(self):
        return self.nome