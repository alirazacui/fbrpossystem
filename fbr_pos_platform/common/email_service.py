import mimetypes
from html import escape
from pathlib import Path
from email.mime.image import MIMEImage

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


def send_platform_email(
    subject,
    body,
    recipient_list,
    html_body=None,
    from_email=None,
    inline_image_path=None,
    inline_image_cid="brand-logo",
):
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
    if inline_image_path:
        image_path = _resolve_logo_file_path(inline_image_path)
        if image_path:
            with image_path.open("rb") as image_file:
                mime_type, _ = mimetypes.guess_type(str(image_path))
                subtype = (mime_type or "image/png").split("/")[-1]
                image = MIMEImage(image_file.read(), _subtype=subtype)
                image.add_header("Content-ID", f"<{inline_image_cid}>")
                image.add_header("Content-Disposition", "inline", filename=image_path.name)
                message.attach(image)
    return message.send()


def _resolve_logo_file_path(logo_path: str | None) -> Path | None:
    if not logo_path:
        return None

    path = Path(logo_path)
    if path.is_dir():
        candidates = sorted(
            [
                candidate
                for candidate in path.iterdir()
                if candidate.is_file() and candidate.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
            ]
        )
        if not candidates:
            return None
        return candidates[0]

    if not path.exists() or not path.is_file():
        return None

    return path


def build_welcome_email_html(
    *,
    brand_name: str,
    logo_path: str | None,
    logo_url: str | None,
    logo_cid: str | None = None,
    recipient_name: str,
    login_url: str,
    username: str,
    password: str,
    welcome_note: str,
) -> str:
    brand_name = escape(brand_name)
    recipient_name = escape(recipient_name or "there")
    username = escape(username)
    password = escape(password)
    login_url = escape(login_url)
    welcome_note = escape(welcome_note)
    logo_markup = ""

    resolved_logo_src = logo_url
    if logo_path and logo_cid:
        image_path = _resolve_logo_file_path(logo_path)
        if image_path:
            resolved_logo_src = f"cid:{logo_cid}"

    if resolved_logo_src:
        logo_markup = f'''
            <div style="text-align:center; margin-bottom:24px;">
                <img src="{escape(resolved_logo_src)}" alt="{brand_name} logo" style="max-width:140px; max-height:64px; object-fit:contain; display:inline-block;" />
            </div>
        '''

    return f"""
        <div style="margin:0; padding:0; background:#f3f7fb; font-family:Arial,Helvetica,sans-serif; color:#0f172a;">
            <div style="max-width:640px; margin:0 auto; padding:32px 16px;">
                <div style="background:#ffffff; border-radius:18px; overflow:hidden; box-shadow:0 10px 30px rgba(15,23,42,0.08); border:1px solid #e2e8f0;">
                    <div style="padding:32px 32px 8px; background:linear-gradient(135deg, #0f766e, #14b8a6); color:#ffffff; text-align:center;">
                        {logo_markup}
                        <div style="font-size:12px; letter-spacing:0.18em; text-transform:uppercase; opacity:0.9;">Welcome to</div>
                        <h1 style="margin:8px 0 0; font-size:30px; line-height:1.2;">{brand_name}</h1>
                    </div>

                    <div style="padding:32px;">
                        <p style="font-size:20px; line-height:1.4; margin:0 0 16px; font-weight:700;">Hello {recipient_name},</p>
                        <p style="font-size:15px; line-height:1.8; margin:0 0 18px; color:#334155;">
                            {welcome_note}
                        </p>

                        <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:16px; padding:20px; margin:24px 0;">
                            <p style="margin:0 0 12px; font-size:14px; color:#475569;">Your login details</p>
                            <table role="presentation" style="width:100%; border-collapse:collapse; font-size:14px;">
                                <tr>
                                    <td style="padding:8px 0; color:#64748b; width:120px;">Username</td>
                                    <td style="padding:8px 0; font-weight:700; color:#0f172a;">{username}</td>
                                </tr>
                                <tr>
                                    <td style="padding:8px 0; color:#64748b;">Password</td>
                                    <td style="padding:8px 0; font-weight:700; color:#0f172a;">{password}</td>
                                </tr>
                            </table>
                        </div>

                        <div style="text-align:center; margin:28px 0;">
                            <a href="{login_url}" style="display:inline-block; background:#0f766e; color:#ffffff; text-decoration:none; padding:14px 24px; border-radius:999px; font-weight:700;">Login to your account</a>
                        </div>

                        <p style="font-size:13px; line-height:1.7; margin:0; color:#64748b;">
                            For security, please change your password after your first login.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """