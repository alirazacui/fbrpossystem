import boto3
from urllib.parse import urlparse
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import models
from .models import FBRSubmissionLog
from common.permissions import IsAdmin
from receipt.generators import A4InvoiceGenerator


def _extract_s3_key(url_or_path: str) -> str:
    if not url_or_path:
        return ""
    parsed = urlparse(url_or_path)
    if parsed.scheme and parsed.netloc:
        return parsed.path.lstrip("/")
    return url_or_path.lstrip("/")


def _presigned_url(key: str, as_attachment: bool = False) -> str:
    client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )
    params = {
        "Bucket": settings.AWS_STORAGE_BUCKET_NAME,
        "Key": key,
    }
    if as_attachment:
        filename = key.split("/")[-1] or "invoice.pdf"
        params["ResponseContentDisposition"] = f'attachment; filename="{filename}"'
    return client.generate_presigned_url("get_object", Params=params, ExpiresIn=300)

class FBRSubmissionAdminViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request):
        qs = FBRSubmissionLog.objects.select_related('company').order_by('-created_at')
        
        # Optional search by local_invoice_id, company name, fbr_invoice_id
        search = request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(
                models.Q(local_invoice_id__icontains=search) |
                models.Q(fbr_invoice_id__icontains=search) |
                models.Q(company__business_name__icontains=search)
            )

        # Basic pagination if needed
        limit = int(request.query_params.get("limit", 100))
        offset = int(request.query_params.get("offset", 0))
        total = qs.count()
        qs = qs[offset:offset+limit]

        results = []
        for log in qs:
            results.append({
                "id": log.id,
                "created_at": timezone.localtime(log.created_at).strftime("%B %d, %Y, %I:%M %p"),
                "company_name": log.company.business_name,
                "local_invoice_id": log.local_invoice_id or "-",
                "fbr_invoice_id": log.fbr_invoice_id or "-",
                "endpoint": log.endpoint,
                "environment": log.environment,
                "status_code": log.status_code or "-",
                "http_status": log.http_status or "-",
                "attempt": log.attempt,
                "latency_ms": log.latency_ms or 0,
                "sale_id": log.sale_id
            })
            
        return Response({"count": total, "results": results})

    def retrieve(self, request, pk=None):
        try:
            log = FBRSubmissionLog.objects.select_related('company').get(pk=pk)
        except FBRSubmissionLog.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        return Response({
            "id": log.id,
            "created_at": timezone.localtime(log.created_at).strftime("%B %d, %Y, %I:%M %p"),
            "company_name": log.company.business_name,
            "local_invoice_id": log.local_invoice_id or "-",
            "fbr_invoice_id": log.fbr_invoice_id or "-",
            "endpoint": log.endpoint,
            "environment": log.environment,
            "status_code": log.status_code or "-",
            "http_status": log.http_status or "-",
            "attempt": log.attempt,
            "latency_ms": log.latency_ms or 0,
            "error_message": log.error_message or "-",
            "request_payload": log.request_payload,
            "response_payload": log.response_payload,
            "sale_id": log.sale_id
        })

    @action(detail=True, methods=["get"], url_path="invoice-pdf")
    def invoice_pdf(self, request, pk=None):
        try:
            log = FBRSubmissionLog.objects.select_related("sale").get(pk=pk)
        except FBRSubmissionLog.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        if not log.sale_id:
            return Response({"error": "No sale is linked to this submission."}, status=404)

        sale = log.sale
        invoice_url = sale.receipt_a4_url
        if not invoice_url:
            generator = A4InvoiceGenerator(sale)
            invoice_url = generator.generate()
            sale.receipt_a4_url = invoice_url
            from django.utils import timezone
            sale.receipt_generated_at = timezone.now()
            sale.save(update_fields=["receipt_a4_url", "receipt_generated_at", "updated_at"])

        key = _extract_s3_key(invoice_url)
        if not key:
            return Response({"error": "Invoice file key not found"}, status=400)

        as_attachment = request.query_params.get("download") == "1"
        presigned = _presigned_url(key, as_attachment=as_attachment)

        return Response({
            "url": presigned,
            "sale_id": sale.id,
            "sale_number": sale.sale_number,
            "download": as_attachment,
        })