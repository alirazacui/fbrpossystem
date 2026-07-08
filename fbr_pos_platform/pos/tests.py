from django.test import TestCase
from rest_framework.test import APIRequestFactory

from common.views import AdminInvoicesView
from companies.models import Company
from pos.models import Customer, Sale
from pos.views import SaleViewSet
from users.models import User, UserStatus


class InvoiceScopeTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.company_a = Company.objects.create(
            business_name="Alpha Retail",
            ntn="1111111111",
            owner_cnic="11111-1111111-1",
        )
        self.company_b = Company.objects.create(
            business_name="Beta Retail",
            ntn="2222222222",
            owner_cnic="22222-2222222-2",
        )

        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="password123",
            role=User.Role.ADMIN,
            status=UserStatus.ACTIVE,
        )
        self.owner_a = User.objects.create_user(
            email="owner_a@example.com",
            password="password123",
            role=User.Role.OWNER,
            company=self.company_a,
            status=UserStatus.ACTIVE,
        )
        self.owner_b = User.objects.create_user(
            email="owner_b@example.com",
            password="password123",
            role=User.Role.OWNER,
            company=self.company_b,
            status=UserStatus.ACTIVE,
        )

        self.customer_a = Customer.objects.create(company=self.company_a, name="Customer A")
        self.customer_b = Customer.objects.create(company=self.company_b, name="Customer B")

        self.sale_a = Sale.objects.create(
            company=self.company_a,
            cashier=self.owner_a,
            customer=self.customer_a,
        )
        self.sale_b = Sale.objects.create(
            company=self.company_b,
            cashier=self.owner_b,
            customer=self.customer_b,
        )

    def _request_for(self, user):
        request = self.factory.get("/api/sales/")
        request.user = user
        return request

    def test_admin_sees_all_sales_for_sale_viewset(self):
        view = SaleViewSet()
        request = self._request_for(self.admin)
        view.request = request

        queryset = view.get_queryset()

        self.assertIn(self.sale_a, queryset)
        self.assertIn(self.sale_b, queryset)

    def test_company_owner_sees_only_their_company_sales(self):
        view = SaleViewSet()
        request = self._request_for(self.owner_a)
        view.request = request

        queryset = view.get_queryset()

        self.assertIn(self.sale_a, queryset)
        self.assertNotIn(self.sale_b, queryset)

    def test_admin_invoices_view_returns_all_sales(self):
        request = self._request_for(self.admin)
        view = AdminInvoicesView()
        view.request = request

        response = view.get(request)

        self.assertEqual(response.status_code, 200)
        returned_ids = {item["id"] for item in response.data}
        self.assertIn(self.sale_a.id, returned_ids)
        self.assertIn(self.sale_b.id, returned_ids)
