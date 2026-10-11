import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(bind=True, name="receipt.bulk_regenerate_invoice_documents")
def bulk_regenerate_invoice_documents(self, sale_ids, include_thermal=True, include_a4=True):
    """
    Regenerate PDF documents only.

    This task intentionally does NOT submit invoices to PRAL/FBR or modify
    fbr_invoice_number / fbr_submission_status. It only refreshes the stored PDF
    URLs used for downloading/printing documents.
    """
    from pos.models import Sale
    from receipt.generators import A4InvoiceGenerator, ThermalReceiptGenerator

    sale_ids = list(sale_ids or [])
    if not sale_ids:
        return {"processed": 0, "sale_ids": []}

    sales = list(
        Sale.objects.select_related("company", "customer", "cashier")
        .filter(id__in=sale_ids)
        .order_by("id")
    )

    processed = 0
    regenerated_a4 = 0
    regenerated_thermal = 0

    for sale in sales:
        try:
            if include_a4:
                A4InvoiceGenerator(sale).generate(force_regenerate=True)
                regenerated_a4 += 1

            if include_thermal:
                ThermalReceiptGenerator(sale).generate(force_regenerate=True)
                regenerated_thermal += 1

            processed += 1
        except Exception:
            logger.exception("Bulk invoice regeneration failed for Sale ID=%s", sale.id)
            continue

    return {
        "processed": processed,
        "requested": len(sale_ids),
        "regenerated_a4": regenerated_a4,
        "regenerated_thermal": regenerated_thermal,
        "sale_ids": [sale.id for sale in sales],
        "note": "PDF-only regeneration; no PRAL/FBR submission was triggered.",
    }
