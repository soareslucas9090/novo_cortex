from django.core.mail import EmailMultiAlternatives

from AppCore.core.exceptions.exceptions import SystemErrorException


def send_simple_email(subject, simple_text, from_email, to_emails, html_content):
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
