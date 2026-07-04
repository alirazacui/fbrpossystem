from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from common.models import PlatformSettings


def _smtp_config():
    config = PlatformSettings.load()
    return {
        "host": config.smtp_host or getattr(settings, "EMAIL_HOST", "smtp.gmail.com"),
        "port": config.smtp_port or getattr(settings, "EMAIL_PORT", 587),
        "use_tls": config.smtp_use_tls,
        "username": config.smtp_username or getattr(settings, "EMAIL_HOST_USER", ""),
        "password": config.smtp_password or getattr(settings, "EMAIL_HOST_PASSWORD", ""),
    }


def send_platform_email(subject, body, recipient_list, html_body=None, from_email=None):
    config = PlatformSettings.load()
    smtp_config = _smtp_config()

    sender = from_email or config.default_from_email or getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@posplatform.pk")
    connection = get_connection(
        backend="django.core.mail.backends.smtp.EmailBackend",
        host=smtp_config["host"],
        port=smtp_config["port"],
        username=smtp_config["username"],
        password=smtp_config["password"],
        use_tls=smtp_config["use_tls"],
        fail_silently=False,
    )

    message = EmailMultiAlternatives(subject, body, sender, recipient_list, connection=connection)
    if html_body:
        message.attach_alternative(html_body, "text/html")
    return message.send()