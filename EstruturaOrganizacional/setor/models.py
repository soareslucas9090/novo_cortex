from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager


class Setor(BasicModel):
    """
    Representa um setor dentro do campus.
    
    Relacionamentos:
    - Setor (1) → (*) Atividade
    - Setor (*) ↔ (*) Usuario (via UsuarioSetor)
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    sigla = models.CharField(
        'Sigla',
        max_length=50,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'setores'
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nome']

    def __str__(self):
        return self.nome
