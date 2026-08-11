from types import SimpleNamespace

from django.test import TestCase

from digital_invoicing.pos_client import resolve_pos_endpoint


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
