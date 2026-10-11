from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, TestCase
from rest_framework.request import Request

from companies.models import Company
from companies.serializers import CompanyDetailSerializer
from common.views import AdminInvoiceDocumentView
from digital_invoicing.pos_client import resolve_pos_endpoint


class CompanyClientTypeSerializerTests(TestCase):
    def test_client_type_is_updatable_via_serializer(self):
        company = Company.objects.create(
            business_name="Test Business",
            ntn="1234567",
            owner_cnic="12345-6789012-3",
            address="Main Street",
            client_type="fbr",
        )

        serializer = CompanyDetailSerializer(
            company,
            data={"client_type": "pra"},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        company.refresh_from_db()
        self.assertEqual(company.client_type, "pra")


class ResolvePosEndpointTests(TestCase):
    def test_uses_production_endpoint_when_available(self):
        company = SimpleNamespace(
            pos_sandbox_endpoint="https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData",
            pos_production_endpoint="https://ims.pral.com.pk/ims/production/api/Live/PostData",
        )

        self.assertEqual(
            resolve_pos_endpoint(company, is_sandbox=False),
            "https://ims.pral.com.pk/ims/production/api/Live/PostData",
        )

    def test_falls_back_to_sandbox_endpoint_for_production_if_needed(self):
        company = SimpleNamespace(
            pos_sandbox_endpoint="https://ims.pral.com.pk/ims/production/api/Live/PostData",
            pos_production_endpoint="",
        )

        self.assertEqual(
            resolve_pos_endpoint(company, is_sandbox=False),
            "https://ims.pral.com.pk/ims/production/api/Live/PostData",
        )


class AdminInvoiceDocumentViewTests(TestCase):
    @patch("common.views.boto3.client")
    @patch("common.views.A4InvoiceGenerator")
    @patch("common.views.Sale.objects.select_related")
    def test_regenerates_cached_invoice_when_serving_document(self, mock_select_related, mock_generator_cls, mock_boto_client):
        sale = SimpleNamespace(
            id=42,
            company=SimpleNamespace(),
            receipt_a4_url="https://example.com/stale-invoice.pdf",
            sale_number="INV-1001",
            save=Mock(),
        )
        mock_select_related.return_value.get.return_value = sale

        mock_generator = mock_generator_cls.return_value
        mock_generator.generate.return_value = "https://example.com/fresh-invoice.pdf"
        mock_boto_client.return_value.generate_presigned_url.return_value = "https://signed.example.com/fresh-invoice.pdf"

        request = Request(
            RequestFactory().get("/admin-dashboard/invoices/42/document/", {"download": "0"})
        )

        response = AdminInvoiceDocumentView().get(request, 42)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["url"], "https://signed.example.com/fresh-invoice.pdf")
        mock_generator.generate.assert_called_once_with(force_regenerate=True)
