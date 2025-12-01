from Vinculos.matricula import *

from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager


class Matricula(BasicModel):
    """
    Representa as matrículas/carteirinhas de um usuário.
    
    Relacionamentos:
    - Usuario (1) → (*) Matricula
    """
    matricula = models.CharField(
        'Número da Matrícula',
        max_length=50,
        unique=True,
        primary_key=True,
    )
    usuario = models.ForeignKey(
        "Usuarios.usuario.Usuario",
        on_delete=models.CASCADE,
        related_name='matriculas',
        verbose_name='Usuário',
    )
    data_validade = models.DateField(
        'Data de Validade',
    )
    data_expedicao = models.DateField(
        'Data de Expedição',
        default=timezone.now,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['usuario', '-data_expedicao']

    def __str__(self):
        return f'{self.usuario.nome} - {self.matricula}'
