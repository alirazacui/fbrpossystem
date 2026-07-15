from django.shortcuts import render

# Create your views here.
"""
========================================================
receipts/views.py
========================================================
"""
 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from django.http import HttpResponse
from common.permissions import IsActiveUser
from .generators import *
 
@api_view(["GET"])
@permission_classes([IsActiveUser])
def get_thermal_receipt(request, sale_id):
    """
    GET /api/receipts/{sale_id}/thermal/
 
    Returns URL of thermal receipt PDF.
    Generates if not already generated.
    """
    from pos.models import Sale, SaleStatus
    try:
        sale = Sale.objects.get(
            pk      = sale_id,
            company = request.user.company,
        )
    except Sale.DoesNotExist:
        return Response(
            {"error": "Sale not found or not completed."},
            status=http_status.HTTP_404_NOT_FOUND,
        )
 
    try:
        generator = ThermalReceiptGenerator(sale)
        url       = generator.generate()
        return Response({"url": url, "type": "thermal"})
    except Exception as e:
        logger.error(f"Thermal receipt generation failed for sale {sale_id}: {e}")
        return Response(
            {"error": f"Receipt generation failed: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
 
 
from django.shortcuts import render

# Create your views here.
"""
========================================================
receipts/views.py
========================================================
"""
 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status as http_status
from django.http import HttpResponse
from common.permissions import IsActiveUser
from .generators import *
 
@api_view(["GET"])
@permission_classes([IsActiveUser])
def get_thermal_receipt(request, sale_id):
    """
    GET /api/receipts/{sale_id}/thermal/
 
    Returns URL of thermal receipt PDF.
    Generates if not already generated.
    """
    from pos.models import Sale, SaleStatus
    try:
        sale = Sale.objects.get(
            pk      = sale_id,
            company = request.user.company,
        )
    except Sale.DoesNotExist:
        return Response(
            {"error": "Sale not found or not completed."},
            status=http_status.HTTP_404_NOT_FOUND,
        )
 
    try:
        generator = ThermalReceiptGenerator(sale)
        url       = generator.generate()
        return Response({"url": url, "type": "thermal"})
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
 
    Returns URL of A4 invoice PDF.
    """
    from pos.models import Sale
    try:
        sale_qs = Sale.objects.filter(pk=sale_id)
        if not request.user.is_platform_admin:
            sale_qs = sale_qs.filter(company=request.user.company)
        sale = sale_qs.get()
    except Sale.DoesNotExist:
        return Response(
            {"error": "Sale not found or not completed."},
            status=http_status.HTTP_404_NOT_FOUND,
        )
 
    try:
        generator = A4InvoiceGenerator(sale)
        # IMPORTANT: force_regenerate=True.
        # generate() only fills generator.buffer with PDF bytes when it actually
        # builds the PDF. If sale.receipt_a4_url was already set from a previous
        # download, generate() short-circuits and returns the cached URL WITHOUT
        # touching the buffer — leaving it empty and producing a 0-byte "PDF".
        # Forcing regeneration guarantees we always have real bytes to send back.
        invoice_url = generator.generate(force_regenerate=True)
        generator.buffer.seek(0)
        response = HttpResponse(generator.buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="invoice_{sale.sale_number or sale.id}.pdf"'
        response['X-Invoice-URL'] = invoice_url
        return response
    except Exception as e:
        logger.error(f"A4 invoice generation failed for sale {sale_id}: {e}")
        return Response(
            {"error": f"Invoice generation failed: {str(e)}"},
            status=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
        )