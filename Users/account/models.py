from django.db import models

from AppCore.basics.models.models import BasicModel


class EmailAccountCode(BasicModel):
    email = models.EmailField('Email')
    code = models.CharField('Código', max_length=6, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_validated = models.BooleanField('Validado', default=False)
    
    class Meta:
        db_table = 'email_account_codes'
        verbose_name = 'Código de verificação de email'
        verbose_name_plural = 'Códigos de verificação de email'
        ordering = ['-created_at']

    def __str__(self):
        return self.email
