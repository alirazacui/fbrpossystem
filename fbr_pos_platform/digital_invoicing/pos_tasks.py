"""
========================================================
digital_invoicing/pos_tasks.py

Celery Tasks for FBR POS Invoice Submission
========================================================
"""

import logging
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="digital_invoicing.submit_invoice_to_fbr_pos",
)
def submit_invoice_to_fbr_pos(self, sale_id: int):
    """
    Background Celery task — submits a completed sale to FBR POS API.

    Called automatically when a sale is completed via SaleViewSet.complete()
    for POS clients (business_mode includes 'pos').

    Args:
        sale_id: Primary key of the Sale to submit

    Flow:
        1. Load Sale + Company from DB
        2. Get POS credentials (POSID, Access Code, endpoint)
        3. Build invoice JSON using POSInvoiceBuilder
        4. POST to FBR POS API via POSClient
        5. Store fbr_invoice_number on Sale
        6. Mark fbr_submission_status = SUCCESS
    On failure:
        7. Store error_code + error_message on Sale
        8. Mark fbr_submission_status = FAILED
        9. Retry up to 3 times on network errors
    """
    from pos.models import Sale, FBRSubmissionStatus
    from .pos_client import POSClient, POSAPIError
    from .pos_invoice_builder import POSInvoiceBuilder
    from .submission_utils import should_keep_existing_submission_result
    from django.utils import timezone

    logger.info(f"[POS Task] Starting submission for Sale ID: {sale_id}")

    # ── Load Sale ────────────────────────────────────────────────────
    try:
        sale = Sale.objects.select_related(
            "company", "customer", "original_sale"
        ).prefetch_related("lines").get(pk=sale_id)
    except Sale.DoesNotExist:
        logger.error(f"[POS Task] Sale {sale_id} not found")
        return

    # ── Guard: only submit COMPLETED sales ───────────────────────────
    from pos.models import SaleStatus
    if sale.status != SaleStatus.COMPLETED:
        logger.warning(f"[POS Task] Sale {sale_id} is not COMPLETED — skipping")
        return

    # ── Guard: Company must have POS enabled ─────────────────────────
    company = sale.company
    if "pos" not in company.business_mode:
        sale.fbr_submission_status = FBRSubmissionStatus.SKIPPED
        sale.save(update_fields=["fbr_submission_status", "updated_at"])
        logger.info(f"[POS Task] POS not enabled for company — skipping")
        return

    # ── Get POS credentials ─────────────────────────────────────────
    is_sandbox = True
    
    # Use production token if available, otherwise sandbox
    if company.pos_production_token and company.pos_access_code:
        is_sandbox = False
        token = company.pos_production_token
        endpoint = company.pos_production_endpoint
    elif company.pos_sandbox_token and company.pos_access_code:
        is_sandbox = True
        token = company.pos_sandbox_token
        endpoint = company.pos_sandbox_endpoint
    else:
        token = None
        endpoint = None

    if not token or not company.pos_id:
        error_msg = "No POS ID, Access Code, or Token configured."
        logger.error(f"[POS Task] {error_msg} for company {company.business_name}")
        sale.fbr_submission_status = FBRSubmissionStatus.FAILED
        sale.fbr_error_code = "NO_CRED"
        sale.fbr_error_message = error_msg
        sale.save(update_fields=[
            "fbr_submission_status", "fbr_error_code",
            "fbr_error_message", "updated_at"
        ])
        return

    # ── Build invoice JSON ───────────────────────────────────────────
    try:
        builder = POSInvoiceBuilder(sale)
        payload = builder.build()
        
        # Print to terminal for debugging
        import json
        print("\n" + "="*50)
        print(f"FBR POS SUBMIT TRIGGERED ({'SANDBOX' if is_sandbox else 'PRODUCTION'})")
        print(f"POS ID: {company.pos_id}")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        print("="*50 + "\n")
        
        logger.debug(f"[POS Task] Invoice payload built: {payload}")
    except Exception as e:
        logger.error(f"[POS Task] Failed to build invoice JSON: {e}")
        sale.fbr_submission_status = FBRSubmissionStatus.FAILED
        sale.fbr_error_code = "BLD_ERR"
        sale.fbr_error_message = str(e)
        sale.save(update_fields=[
            "fbr_submission_status", "fbr_error_code",
            "fbr_error_message", "updated_at"
        ])
        return

    # ── Submit to FBR POS API ──────────────────────────────────────
    client = POSClient(
        pos_id=company.pos_id,
        access_code=token,
        base_url=endpoint,
        is_sandbox=is_sandbox
    )

    import time
    from .models import FBRSubmissionLog
    start_time = time.time()
    
    status_code = None
    error_message_log = ""
    fbr_invoice_number_log = ""
    raw_response_log = {}
    
    try:
        result = client.submit_invoice(payload)
        latency_ms = int((time.time() - start_time) * 1000)
        
        fbr_invoice_number_log = result.get("fbr_invoice_number", "")
        raw_response_log = result.get("raw_response", {})

        # ── SUCCESS ──────────────────────────────────────────────────
        sale.fbr_submission_status = FBRSubmissionStatus.SUCCESS
        sale.fbr_invoice_number = result["fbr_invoice_number"]
        sale.fbr_qr_code = result["fbr_invoice_number"]  # POS uses invoice number as QR
        sale.fbr_submitted_at = timezone.now()
        sale.fbr_error_code = ""
        sale.fbr_error_message = ""
        sale.save(update_fields=[
            "fbr_submission_status",
            "fbr_invoice_number",
            "fbr_qr_code",
            "fbr_submitted_at",
            "fbr_error_code",
            "fbr_error_message",
            "updated_at",
        ])
        
        from companies.models import AuditLog
        AuditLog.objects.create(
            company=company,
            user_email="system@fbr-pos-worker",
            entity_type="fbr_pos_submission",
            entity_id=str(sale.pk),
            action="submit",
            ip_address="127.0.0.1"
        )
        
        # ── Decrement Stock ──
        from django.db import transaction
        with transaction.atomic():
            for line in sale.lines.select_related("product").all():
                product = line.product
                if product.track_inventory:
                    product.refresh_from_db()
                    product.current_stock = (
                        float(product.current_stock) - float(line.quantity)
                    )
                    product.save(update_fields=["current_stock", "updated_at"])
                        
        logger.info(
            f"[POS Task] ✓ Sale {sale_id} submitted. "
            f"FBR Invoice: {result['fbr_invoice_number']}"
        )

    except ConnectionError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        error_message_log = str(e)
        # Network error — retry
        logger.warning(
            f"[POS Task] Network error for Sale {sale_id}: {e}. "
            f"Retry {self.request.retries + 1}/{self.max_retries}"
        )
        sale.fbr_submission_status = FBRSubmissionStatus.FAILED
        sale.fbr_error_code = "NET_ERR"
        sale.fbr_error_message = str(e)
        sale.save(update_fields=[
            "fbr_submission_status", "fbr_error_code",
            "fbr_error_message", "updated_at"
        ])
        
        # Log Submission
        FBRSubmissionLog.objects.create(
            company=company,
            sale=sale,
            environment="pos_sandbox" if is_sandbox else "pos_production",
            endpoint="PostData",
            local_invoice_id=sale.sale_number,
            fbr_invoice_id="",
            status_code="NET_ERR",
            http_status=None,
            attempt=self.request.retries + 1,
            latency_ms=latency_ms,
            error_message=error_message_log,
            request_payload=payload,
            response_payload={}
        )
        
        try:
            raise self.retry(exc=e)
        except MaxRetriesExceededError:
            logger.error(
                f"[POS Task] Max retries exceeded for Sale {sale_id}. "
                f"Manual resubmission required."
            )

    except POSAPIError as e:
        latency_ms = int((time.time() - start_time) * 1000)
        status_code = str(e.error_code)[:10] if e.error_code else "UNK"
        error_message_log = e.message
        raw_response_log = getattr(e, 'raw_response', {})
        
        # FBR returned an error — don't retry (it's a data issue, not network)
        logger.error(
            f"[POS Task] FBR POS API error for Sale {sale_id}: "
            f"[{e.error_code}] {e.message}"
        )
        if should_keep_existing_submission_result(sale):
            logger.info(
                f"[POS Task] Keeping existing successful submission for Sale {sale_id}; ignoring new API error"
            )
            sale.fbr_error_code = status_code
            sale.fbr_error_message = e.message
            sale.save(update_fields=["fbr_error_code", "fbr_error_message", "updated_at"])
        else:
            sale.fbr_submission_status = FBRSubmissionStatus.FAILED
            sale.fbr_error_code = status_code
            sale.fbr_error_message = e.message
            sale.save(update_fields=[
                "fbr_submission_status", "fbr_error_code",
                "fbr_error_message", "updated_at"
            ])

        from companies.models import AuditLog
        AuditLog.objects.create(
            company=company,
            user_email="system@fbr-pos-worker",
            entity_type="fbr_pos_submission",
            entity_id=str(sale.pk),
            action="fail",
            ip_address="127.0.0.1"
        )
        
    except Exception as e:
        logger.error(f"[POS Task] Unexpected error for Sale {sale_id}: {e}")
        sale.fbr_submission_status = FBRSubmissionStatus.FAILED
        sale.fbr_error_code = "UNK_ERR"
        sale.fbr_error_message = str(e)
        sale.save(update_fields=[
            "fbr_submission_status", "fbr_error_code",
            "fbr_error_message", "updated_at"
        ])

    finally:
        # Save success or POSAPIError logs
        if not error_message_log and fbr_invoice_number_log:
            FBRSubmissionLog.objects.create(
                company=company,
                sale=sale,
                environment="pos_sandbox" if is_sandbox else "pos_production",
                endpoint="PostData",
                local_invoice_id=sale.sale_number,
                fbr_invoice_id=fbr_invoice_number_log,
                status_code="00",
                http_status=200,
                attempt=self.request.retries + 1,
                latency_ms=latency_ms,
                error_message="",
                request_payload=payload,
                response_payload=raw_response_log
            )
        elif status_code and status_code != "NET_ERR":
            FBRSubmissionLog.objects.create(
                company=company,
                sale=sale,
                environment="pos_sandbox" if is_sandbox else "pos_production",
                endpoint="PostData",
                local_invoice_id=sale.sale_number,
                fbr_invoice_id="",
                status_code=status_code,
                http_status=200,
                attempt=self.request.retries + 1,
                latency_ms=latency_ms,
                error_message=error_message_log,
                request_payload=payload,
                response_payload=raw_response_log
            )


@shared_task(name="digital_invoicing.retry_failed_pos_submissions")
def retry_failed_pos_submissions():
    """
    Periodic task — retries all FAILED FBR POS submissions.

    Runs every 15 minutes via Celery Beat.
    Only retries sales that:
    - Are COMPLETED
    - Have fbr_submission_status = FAILED
    - Company has POS enabled (business_mode includes 'pos')
    - Have valid POS credentials set
    - Were last attempted more than 5 minutes ago
    """
    from pos.models import Sale, SaleStatus, FBRSubmissionStatus
    from django.utils import timezone
    from datetime import timedelta

    cutoff = timezone.now() - timedelta(minutes=5)

    failed_sales = Sale.objects.filter(
        status=SaleStatus.COMPLETED,
        fbr_submission_status=FBRSubmissionStatus.FAILED,
        company__business_mode__contains="pos",
        updated_at__lt=cutoff,
    ).select_related("company")

    count = 0
    for sale in failed_sales:
        # Only retry if company has POS credentials
        company = sale.company
        has_credentials = (
            company.pos_id and
            company.pos_access_code and
            (company.pos_production_token or company.pos_sandbox_token)
        )
        if has_credentials:
            submit_invoice_to_fbr_pos.delay(sale.id)
            count += 1

    logger.info(f"[POS Retry Task] Queued {count} failed sales for resubmission")
    return count


@shared_task(name="digital_invoicing.resubmit_single_pos_sale")
def resubmit_single_pos_sale(sale_id: int):
    """
    Manually triggered resubmission for a single sale.
    Called from the admin UI "Resubmit to FBR POS" button.
    """
    from pos.models import Sale, FBRSubmissionStatus
    try:
        sale = Sale.objects.get(pk=sale_id)
        # Reset status to pending before resubmitting
        sale.fbr_submission_status = FBRSubmissionStatus.PENDING
        sale.fbr_error_code = ""
        sale.fbr_error_message = ""
        sale.save(update_fields=[
            "fbr_submission_status", "fbr_error_code",
            "fbr_error_message", "updated_at"
        ])
        submit_invoice_to_fbr_pos.delay(sale_id)
        logger.info(f"[POS] Manual resubmission queued for Sale {sale_id}")
    except Sale.DoesNotExist:
        logger.error(f"[POS] Sale {sale_id} not found for resubmission")
