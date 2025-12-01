from django.core.mail import EmailMultiAlternatives

from AppCore.core.exceptions.exceptions import SystemErrorException


def enviar_email_simples(subject, simple_text, from_email, to_emails, html_content):
    try:
        email = EmailMultiAlternatives(
            subject,
            simple_text,
            from_email,
            to_emails,
        )

        email.attach_alternative(html_content, "text/html")

        email.send()
    except Exception as err:
        raise SystemErrorException(f'Erro ao enviar email: {err}')


def _formatar_cpf(cpf):
        """Formata o CPF (XXX.XXX.XXX-XX)."""
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf
