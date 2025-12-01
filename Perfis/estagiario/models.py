from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager


class Estagiario(BasicModel):
    """
    Representa um estagiário na instituição.
    
    Herança via OneToOne:
    - Usuario ← Estagiario
    
    Relacionamentos:
    - Empresa (1) → (*) Estagiario
    - Curso (1) → (*) Estagiario
    
    Campos do DER:
    - carga_horaria (INTEGER)
    - data_inicio_estagio (DATE)
    - data_fim_estagio (DATE)
    """
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='estagiario',
        verbose_name='Usuário',
        primary_key=True,
    )
    empresa = models.ForeignKey(
        "empresa.Empresa",
        on_delete=models.PROTECT,
        related_name='estagiarios',
        verbose_name='Empresa/Instituição',
    )
    curso = models.ForeignKey(
        "curso.Curso",
        on_delete=models.PROTECT,
        related_name='estagiarios',
        verbose_name='Curso',
    )
    carga_horaria = models.IntegerField(
        'Carga Horária',
        help_text='Carga horária semanal do estágio',
    )
    data_inicio_estagio = models.DateField(
        'Data de Início do Estágio',
    )
    data_fim_estagio = models.DateField(
        'Data de Fim do Estágio',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'estagiarios'
        verbose_name = 'Estagiário'
        verbose_name_plural = 'Estagiários'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.curso.nome}'
