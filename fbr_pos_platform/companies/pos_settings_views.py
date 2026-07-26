"""
companies/pos_settings_views.py

ViewSet for POS FBR Settings page.
Client enters their POS credentials here after login.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Company
from .pos_settings_serializer import POSFBRSettingsSerializer


class POSFBRSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet for POS FBR Settings page.

    Client can:
    - View their POS FBR settings
    - Update their POS credentials (POS ID, Access Code, Tokens)
    - Test connection using either saved OR request-supplied credentials
    """

    serializer_class = POSFBRSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Only return the user's own company."""
        user = self.request.user
        if user.company:
            return Company.objects.filter(id=user.company.id)
        return Company.objects.none()

    def list(self, request, *args, **kwargs):
        """
        GET /api/pos-fbr-settings/
        Returns the current POS FBR settings for the user's company.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"error": "No company found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        company = queryset.first()
        serializer = self.get_serializer(company)
        return Response(serializer.data)

    @action(detail=False, methods=["put", "patch", "post"])
    def save(self, request, *args, **kwargs):
        """
        PUT/PATCH/POST /api/pos-fbr-settings/save/
        Updates the POS FBR settings for the user's company.
        Using a custom action because DRF maps PUT to detail URLs (/pk/)
        by default, but this is a singleton resource (user's own company).
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"error": "No company found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        company = queryset.first()

        serializer = self.get_serializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def test_connection(self, request):
        """
        POST /api/pos-fbr-settings/test_connection/

        Tests the FBR POS endpoint connection.

        Accepts credentials directly in the request body so the user
        can test WITHOUT saving first:
          {
            "pos_id": "194444",
            "token": "840a2665-...",          # bearer token
            "endpoint": "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData"
          }

        If request body fields are missing, falls back to saved company fields.
        """
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response(
                {"error": "No company found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        company = queryset.first()

        # -----------------------------------------------------------------
        # Resolve credentials: prefer request body → fall back to DB values
        # FBR POS V2.1 uses a single UUID bearer token for everything.
        # The frontend sends it as "token" (or "pos_sandbox_token").
        # -----------------------------------------------------------------
        pos_id = (
            request.data.get("pos_id")
            or company.pos_id
        )
        token = (
            request.data.get("token")
            or request.data.get("pos_sandbox_token")
            or request.data.get("pos_production_token")
            or company.pos_sandbox_token
            or company.pos_production_token
            or company.pos_access_code
        )
        endpoint = (
            request.data.get("endpoint")
            or request.data.get("pos_sandbox_endpoint")
            or company.pos_sandbox_endpoint
            or "https://esp.fbr.gov.pk:8244/FBR/v1/api/Live/PostData"
        )

        import logging
        logger = logging.getLogger(__name__)
        logger.info(
            f"[POS Test] pos_id={pos_id} endpoint={endpoint} "
            f"token_prefix={str(token)[:8] if token else 'NONE'}..."
        )

        if not pos_id:
            return Response(
                {"success": False, "message": "POS ID is required. Enter it in the form."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not token:
            return Response(
                {"success": False, "message": "Token is required. Enter the Bearer Token (UUID) in the form."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            from digital_invoicing.pos_client import POSClient

            client = POSClient(
                pos_id=str(pos_id),
                access_code=str(token),
                base_url=str(endpoint),
                is_sandbox=True,
            )

            result = client.test_connection()

            logger.info(f"[POS Test] Result: {result}")

            http_status = status.HTTP_200_OK if result["success"] else status.HTTP_400_BAD_REQUEST
            return Response(result, status=http_status)

        except Exception as e:
            logger.exception(f"[POS Test] Unexpected error: {e}")
            return Response(
                {"success": False, "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
