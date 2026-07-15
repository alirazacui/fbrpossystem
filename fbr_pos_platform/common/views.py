from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsAdmin
from django.conf import settings
from urllib.parse import urlparse
import boto3
from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta

from companies.models import Company, AuditLog
from users.models import User
from subscriptions.models import CompanySubscription
from pos.models import Sale
from digital_invoicing.models import FBRSubmissionLog
from common.models import PlatformSettings
from common.serializers import PlatformSettingsSerializer, AdminPasswordChangeSerializer
from receipt.generators import A4InvoiceGenerator

class AdminDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        
        # Summary
        total_tenants = Company.objects.count()
        active_tenants = Company.objects.filter(is_active=True).count()
        total_users = User.objects.count()
        total_managers = User.objects.filter(role=User.Role.MANAGER).count()
        total_cashiers = User.objects.filter(role=User.Role.CASHIER).count()
        total_salespersons = User.objects.filter(role=User.Role.SALESPERSON).count()
        active_subs = CompanySubscription.objects.filter(status='active').count()
        total_invoices = Sale.objects.filter(fbr_submission_status='SUCCESS').count()
        total_fbr_submissions = FBRSubmissionLog.objects.count()

        # FBR Chart (Last 30 days)
        fbr_chart = (
            FBRSubmissionLog.objects.filter(created_at__gte=thirty_days_ago)
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(count=Count('id'))
            .order_by('date')
        )

        chart_data = {
            "labels": [],
            "values": []
        }
        for entry in fbr_chart:
            if entry['date']:
                chart_data["labels"].append(entry['date'].strftime("%b %d"))
                chart_data["values"].append(entry['count'])

        # Recent Subscriptions expiring
        expiring_subs_qs = CompanySubscription.objects.filter(
            status='active', 
            expiry_date__lte=now + timedelta(days=30)
        ).select_related('company', 'plan').order_by('expiry_date')[:5]
        
        expiring_subs = [
            {
                "company_name": sub.company.business_name if sub.company else 'Unknown',
                "plan": sub.plan.name if sub.plan else 'Unknown',
                "expires_on": sub.expiry_date.strftime("%Y-%m-%d") if sub.expiry_date else 'Unknown'
            }
            for sub in expiring_subs_qs
        ]

        # Recent Failed FBR
        failed_fbr_qs = FBRSubmissionLog.objects.filter(
            Q(status_code__isnull=True) | ~Q(status_code__in=['00', '0'])
        ).order_by('-created_at')[:5]

        failed_fbr = [
            {
                "sale_id": log.sale_id,
                "endpoint": log.endpoint,
                "status_code": log.status_code,
                "attempted_at": timezone.localtime(log.created_at).strftime("%Y-%m-%d %H:%M")
            }
            for log in failed_fbr_qs
        ]

        # Recent Activity (Latest companies created)
        recent_companies = Company.objects.order_by('-created_at')[:5]
        recent_activity = [
            {
                "message": f"New tenant '{comp.business_name}' registered.",
                "date": timezone.localtime(comp.created_at).strftime("%Y-%m-%d %H:%M")
            }
            for comp in recent_companies
        ]

        return Response({
            "metrics": {
                "total_tenants": total_tenants,
                "active_tenants": active_tenants,
                "total_users": total_users,
                "total_managers": total_managers,
                "total_cashiers": total_cashiers,
                "total_salespersons": total_salespersons,
                "active_subscriptions": active_subs,
                "successful_invoices": total_invoices,
                "total_fbr_submissions": total_fbr_submissions,
            },
            "chart_data": chart_data,
            "expiring_subscriptions": expiring_subs,
            "failed_fbr": failed_fbr,
            "recent_activity": recent_activity
        })


class PlatformSettingsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        settings_obj = PlatformSettings.load()
        return Response(PlatformSettingsSerializer(settings_obj).data)

    def patch(self, request):
        settings_obj = PlatformSettings.load()
        serializer = PlatformSettingsSerializer(settings_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = AdminPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data["current_password"]):
            return Response({"current_password": "Current password is incorrect."}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save(update_fields=["password", "username", "is_active", "updated_at"])
        return Response({"detail": "Admin password updated successfully."})

class AdminFbrTokensView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        companies = Company.objects.all().order_by('-created_at')
        tokens_list = []
        
        for company in companies:
            # Production row
            tokens_list.append({
                "id": f"{company.id}-prod",
                "tenant_name": company.business_name,
                "environment": "Production",
                "is_active": bool(company.fbr_production_token),
                "created_at": company.created_at,
                "updated_at": company.updated_at
            })
            # Sandbox row
            tokens_list.append({
                "id": f"{company.id}-sandbox",
                "tenant_name": company.business_name,
                "environment": "Sandbox",
                "is_active": bool(company.fbr_sandbox_token),
                "created_at": company.created_at,
                "updated_at": company.updated_at
            })

        return Response(tokens_list)

class AdminFbrTokenDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, token_id):
        # format: "{company_id}-prod" or "{company_id}-sandbox"
        try:
            parts = token_id.split("-")
            env = parts[-1]
            company_id = "-".join(parts[:-1])
            company = Company.objects.get(id=company_id)
        except (ValueError, Company.DoesNotExist):
            return Response({"error": "Token not found"}, status=404)

        if env == "prod":
            data = {
                "id": f"{company.id}-prod",
                "tenant_name": company.business_name,
                "environment": "Production",
                "is_active": bool(company.fbr_production_token),
                "token_encrypted": company.fbr_production_token,
                "api_endpoint": company.fbr_production_endpoint,
                "licensed_integrator": "PRAL",
                "activated_at": company.created_at, # Fallback
                "expires_at": None,
                "created_at": company.created_at,
                "updated_at": company.updated_at
            }
        else:
            data = {
                "id": f"{company.id}-sandbox",
                "tenant_name": company.business_name,
                "environment": "Sandbox",
                "is_active": bool(company.fbr_sandbox_token),
                "token_encrypted": company.fbr_sandbox_token,
                "api_endpoint": company.fbr_sandbox_endpoint,
                "licensed_integrator": "PRAL",
                "activated_at": company.created_at, # Fallback
                "expires_at": None,
                "created_at": company.created_at,
                "updated_at": company.updated_at
            }
        
        return Response(data)

class AdminInvoicesView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # Fetch all sales, ideally paginated, but for now we limit to 500 or just return all
        sales = Sale.objects.select_related('company', 'customer').order_by('-created_at')[:500]
        
        invoices_list = []
        for sale in sales:
            invoices_list.append({
                "id": sale.id,
                "tenant_name": sale.company.business_name if sale.company else "Unknown",
                "invoice_number": sale.sale_number,
                "fbr_invoice_number": sale.fbr_invoice_number,
                "status": sale.status,
                "fbr_status": sale.fbr_submission_status,
                "total_amount": float(sale.total_amount),
                "created_at": sale.created_at,
                "document_ready": bool(sale.receipt_a4_url),
            })
            
        return Response(invoices_list)


class AdminInvoiceDocumentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def _extract_s3_key(self, url_or_path: str) -> str:
        if not url_or_path:
            return ""
        parsed = urlparse(url_or_path)
        if parsed.scheme and parsed.netloc:
            return parsed.path.lstrip("/")
        return url_or_path.lstrip("/")

    def _presigned_url(self, key: str, as_attachment: bool = False) -> str:
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

        return client.generate_presigned_url(
            "get_object",
            Params=params,
            ExpiresIn=300,
        )

    def get(self, request, sale_id):
        try:
            sale = Sale.objects.select_related("company").get(id=sale_id)
        except Sale.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=404)

        if not sale.receipt_a4_url:
            generator = A4InvoiceGenerator(sale)
            sale.receipt_a4_url = generator.generate()
            sale.save(update_fields=["receipt_a4_url", "receipt_generated_at", "updated_at"])

        key = self._extract_s3_key(sale.receipt_a4_url)
        if not key:
            return Response({"error": "Invoice file key not found"}, status=400)

        as_attachment = request.query_params.get("download") == "1"
        presigned = self._presigned_url(key, as_attachment=as_attachment)
        return Response({
            "url": presigned,
            "sale_id": sale.id,
            "sale_number": sale.sale_number,
            "download": as_attachment,
        })

class AdminAuditLogsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        logs = AuditLog.objects.select_related('company').order_by('-created_at')[:500]
        
        logs_list = []
        for log in logs:
            logs_list.append({
                "id": log.id,
                "created_at": log.created_at,
                "tenant_name": log.company.business_name if log.company else "Unknown",
                "user_email": log.user_email,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "action": log.action
            })
            
        return Response(logs_list)

class AdminAuditLogDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, log_id):
        try:
            log = AuditLog.objects.select_related('company').get(id=log_id)
        except AuditLog.DoesNotExist:
            return Response({"error": "Audit log not found"}, status=404)

        data = {
            "id": log.id,
            "created_at": log.created_at,
            "tenant_name": log.company.business_name if log.company else "Unknown",
            "user_email": log.user_email,
            "entity_type": log.entity_type,
            "entity_id": log.entity_id,
            "action": log.action,
            "before_data": None,
            "after_data": None, # our model doesn't store payload yet
            "changes": None,
            "ip_address": log.ip_address,
            "user_agent": None
        }
        
        return Response(data)
