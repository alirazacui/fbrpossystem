from celery import shared_task

from common.email_service import send_platform_email


@shared_task(name="common.send_platform_email")
def send_platform_email_task(
    subject,
    body,
    recipient_list,
    html_body=None,
    from_email=None,
    inline_image_path=None,
    inline_image_cid="brand-logo",
):
    return send_platform_email(
        subject,
        body,
        recipient_list,
        html_body=html_body,
        from_email=from_email,
        inline_image_path=inline_image_path,
        inline_image_cid=inline_image_cid,
    )