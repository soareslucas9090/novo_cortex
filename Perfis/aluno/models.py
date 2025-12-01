from django.db import models

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager

from . import choices


class Aluno(BasicModel):
    """
    Representa um aluno da instituição.
    
    Herança via OneToOne:
    - Usuario ← Aluno
    
    Campos do DER:
    - ira (DOUBLE)
    - forma_ingresso (VARCHAR)
    - previsao_conclusao (INTEGER)
    - aluno_especial (BOOLEAN)
    - turno (VARCHAR)
    - is_active (BOOLEAN)
    - ano_conclusao (INTEGER)
    - data_colacao (DATE)
    - data_expedicao_diploma (DATE)
    """
    usuario = models.OneToOneField(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='aluno',
        verbose_name='Usuário',
        primary_key=True,
    )
    ira = models.DecimalField(
        'IRA',
        max_digits=4,
        decimal_places=2,
        default=0.00,
        help_text='Índice de Rendimento Acadêmico (0.00 a 10.00)',
    )
    forma_ingresso = models.CharField(
        'Forma de Ingresso',
        max_length=20,
        choices=choices.FORMA_INGRESSO_OPCOES,
        default=choices.FORMA_INGRESSO_ENEM,
    )
    previsao_conclusao = models.IntegerField(
        'Previsão de Conclusão',
        help_text='Ano previsto para conclusão do curso',
    )
    aluno_especial = models.BooleanField(
        'Aluno Especial',
        default=False,
    )
    turno = models.CharField(
        'Turno',
        max_length=20,
        choices=choices.TURNO_OPCOES,
        default=choices.TURNO_INTEGRAL,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )
    # Campos de conclusão (quando o aluno se forma)
    ano_conclusao = models.IntegerField(
        'Ano de Conclusão',
        blank=True,
        null=True,
    )
    data_colacao = models.DateField(
        'Data de Colação',
        blank=True,
        null=True,
    )
    data_expedicao_diploma = models.DateField(
        'Data de Expedição do Diploma',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'alunos'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - IRA: {self.ira}'

    @property
    def is_formado(self):
        """Verifica se o aluno já se formou."""
        return self.ano_conclusao is not None