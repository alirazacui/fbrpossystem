import base64

from celery import shared_task
from django.core.files.base import ContentFile

from companies.models import Company


@shared_task(name="companies.upload_company_logo_to_s3")
def upload_company_logo_to_s3(company_id, logo_base64, filename, content_type=None):
    """Upload a company logo to S3 in the background."""
    company = Company.objects.get(id=company_id)
    file_bytes = base64.b64decode(logo_base64)
    content_file = ContentFile(file_bytes)
    content_file.name = filename or "logo.png"

    company.logo.save(content_file.name, content_file, save=True)
    return {
        "company_id": company_id,
        "filename": content_file.name,
        "content_type": content_type,
    }
