"""
========================================================
receipts/views.py
========================================================
"""

import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from django.http import HttpResponse
from common.permissions import IsActiveUser
from .generators import ThermalReceiptGenerator, A4InvoiceGenerator

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([IsActiveUser])
def get_thermal_receipt(request, sale_id):
    """
    GET /api/receipts/{sale_id}/thermal/

    Generates an 80mm thermal receipt and streams the PDF bytes directly
    to the browser so it can be opened in a new tab (same pattern as A4).
    """
    from pos.models import Sale
    try:
        sale = Sale.objects.get(
            pk      = sale_id,
            company = request.user.company,
        )
    except Sale.DoesNotExist:
        return Response(
            {"error": "Sale not found."},
            status=http_status.HTTP_404_NOT_FOUND,
        )

    try:
        generator = ThermalReceiptGenerator(sale)
        # force_regenerate=True so we always get fresh bytes in the buffer
        generator.generate(force_regenerate=True)
        generator.buffer.seek(0)
        response = HttpResponse(generator.buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = (
            f'inline; filename="receipt_{sale.sale_number or sale.id}_thermal.pdf"'
        )
        return response
    except Exception as e:
        logger.error(f"Thermal receipt generation failed for sale {sale_id}: {e}")
        return Response(
            {"error": f"Receipt generation failed: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsActiveUser])
def get_a4_invoice(request, sale_id):
    """
    GET /api/receipts/{sale_id}/a4/

    Generates the full A4 invoice and streams PDF bytes directly to the browser.
    """
    from pos.models import Sale
    try:
        sale_qs = Sale.objects.filter(pk=sale_id)
        if not request.user.is_platform_admin:
            sale_qs = sale_qs.filter(company=request.user.company)
        sale = sale_qs.get()
    except Sale.DoesNotExist:
        return Response(
            {"error": "Sale not found."},
            status=http_status.HTTP_404_NOT_FOUND,
        )

    try:
        generator = A4InvoiceGenerator(sale)
        # force_regenerate=True ensures the buffer is always populated with fresh bytes
        # even if a cached URL already exists on the sale record.
        invoice_url = generator.generate(force_regenerate=True)
        generator.buffer.seek(0)
        response = HttpResponse(generator.buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = (
            f'inline; filename="invoice_{sale.sale_number or sale.id}.pdf"'
        )
        response['X-Invoice-URL'] = invoice_url
        return response
    except Exception as e:
        logger.error(f"A4 invoice generation failed for sale {sale_id}: {e}")
        return Response(
            {"error": f"Invoice generation failed: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )