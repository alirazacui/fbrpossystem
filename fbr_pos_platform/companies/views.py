from django.shortcuts import render

# Create your views here.
"""
========================================================
companies/views.py
========================================================
"""
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import BasePermission
from rest_framework import serializers
 
from common.permissions import IsAdmin, IsAdminOrAdminStaff, IsOwnerOrAdmin
from .models import Company, Branch, Warehouse
from .models import Company, Branch, Warehouse, Terminal
from .serializers import (
    CompanyDetailSerializer,
    CompanyListSerializer,
    CompanyModulesSerializer,
    CompanyPaymentMethodSettingsSerializer,
    BranchSerializer,
    TerminalSerializer,
    WarehouseSerializer,
)
from common.serializers import CompanyOwnerPasswordChangeSerializer
from users.models import User


class IsCompanyOwnerOrAdmin(BasePermission):
    """
    Checks that the user is the owner of the specific company object being accessed,
    or is a platform admin.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_platform_admin:
            return True
        return (
            request.user.role == "owner"
            and request.user.status == "active"
            and obj.id == request.user.company_id
        )


class BranchViewSet(ModelViewSet):
    """
    CRUD for branches under a company.
    Requires user to be authenticated and belong to a company.
    Platform admins can manage branches for any company (though not explicitly handled via query params here, typically handled by setting company manually).
    """
    serializer_class = BranchSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            # For admin, we should optionally filter by company_id query param if needed
            company_id = self.request.query_params.get("company_id")
            if company_id:
                return Branch.objects.filter(company_id=company_id)
            return Branch.objects.all()
        elif user.company_id:
            return Branch.objects.filter(company_id=user.company_id)
        return Branch.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_platform_admin:
            # Requires company to be passed in data (handled by frontend)
            company_id = self.request.data.get("company_id")
            if not company_id:
                raise serializers.ValidationError({"company_id": "Required for platform admins."})
            serializer.save(company_id=company_id)
        else:
            if not getattr(user.company, 'module_multi_branch', False):
                raise serializers.ValidationError({"detail": "Multi-Branch module is not enabled for your company."})
            serializer.save(company=user.company)


class WarehouseViewSet(ModelViewSet):
    """
    CRUD for warehouses under a company.
    Only accessible if the tenant has module_warehousing=True.
    Admins can access all warehouses, optionally filtered by company_id.
    """
    serializer_class = WarehouseSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            company_id = self.request.query_params.get("company_id")
            if company_id:
                return Warehouse.objects.filter(company_id=company_id).select_related('branch')
            return Warehouse.objects.all().select_related('branch')
        elif user.company_id:
            return Warehouse.objects.filter(company_id=user.company_id).select_related('branch')
        return Warehouse.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_platform_admin:
            company_id = self.request.data.get("company_id")
            if not company_id:
                raise serializers.ValidationError({"company_id": "Required for platform admins."})
            serializer.save(company_id=company_id)
        else:
            if not getattr(user.company, 'module_warehousing', False):
                raise serializers.ValidationError({"detail": "Warehousing module is not enabled for your company. Contact your admin."})
            serializer.save(company=user.company)


class TerminalViewSet(ModelViewSet):
    """
    CRUD for POS terminals under a company.
    Owners can only manage terminals if their company has terminals & cash sessions enabled.
    Platform admins can manage all terminals.
    """
    serializer_class = TerminalSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_platform_admin:
            company_id = self.request.query_params.get("company_id")
            queryset = Terminal.objects.select_related("company", "branch")
            if company_id:
                return queryset.filter(company_id=company_id)
            return queryset.all()

        if not user.company_id:
            return Terminal.objects.none()

        if not getattr(user.company, "module_terminals_cash_sessions", False):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Your company does not have the terminals module enabled.")

        return Terminal.objects.filter(company_id=user.company_id).select_related("company", "branch")

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_platform_admin:
            if not getattr(user.company, 'module_terminals_cash_sessions', False):
                raise serializers.ValidationError({"detail": "Terminals & Cash Sessions module is not enabled for your company."})
        serializer.save()


class CompanyViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
    # No DestroyModelMixin — companies are never hard-deleted
):
    """
    Admin-only for list/create, Owner or Admin for retrieve/update.
  
    list    GET  /api/companies/
    create  POST /api/companies/
    retrieve GET /api/companies/{id}/
    update  PUT  /api/companies/{id}/
    partial_update PATCH /api/companies/{id}/
    modules PATCH /api/companies/{id}/modules/   ← toggle feature modules
    activate POST /api/companies/{id}/activate/
    deactivate POST /api/companies/{id}/deactivate/
    """
    queryset         = Company.objects.all().order_by("-created_at")
 
    def get_permissions(self):
        if self.action in ["retrieve", "update", "partial_update", "payment_settings"]:
            return [IsCompanyOwnerOrAdmin()]
        return [IsAdmin()]
 
    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        if self.action == "modules":
            return CompanyModulesSerializer
        return CompanyDetailSerializer
 
    # ── Custom actions ─────────────────────────────────────────────────
 
    @action(detail=True, methods=["patch"], url_path="modules")
    def modules(self, request, pk=None):
        """PATCH /api/companies/{id}/modules/ — toggle feature modules."""
        company    = self.get_object()
        serializer = CompanyModulesSerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
    @action(detail=True, methods=["post"], url_path="activate")
    def activate(self, request, pk=None):
        """POST /api/companies/{id}/activate/"""
        company           = self.get_object()
        company.is_active = True
        company.save(update_fields=["is_active", "updated_at"])
        return Response({"detail": f"'{company.business_name}' has been activated."})
 
    @action(detail=True, methods=["post"], url_path="deactivate")
    def deactivate(self, request, pk=None):
        """POST /api/companies/{id}/deactivate/"""
        company           = self.get_object()
        company.is_active = False
        company.save(update_fields=["is_active", "updated_at"])
        return Response({"detail": f"'{company.business_name}' has been deactivated."})

    @action(detail=True, methods=["post"], url_path="owner-password")
    def owner_password(self, request, pk=None):
        """POST /api/companies/{id}/owner-password/"""
        company = self.get_object()
        serializer = CompanyOwnerPasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        owner = User.objects.filter(company=company, role=User.Role.OWNER).first()
        if not owner:
            return Response({"detail": "Owner account not found for this tenant."}, status=404)

        owner.set_password(serializer.validated_data["new_password"])
        owner.save(update_fields=["password", "username", "is_active", "updated_at"])
        return Response({"detail": "Owner password updated successfully."})

    @action(detail=True, methods=["get", "patch"], url_path="payment-settings")
    def payment_settings(self, request, pk=None):
        """GET or PATCH /api/companies/{id}/payment-settings/"""
        company = self.get_object()
        from pos.models import CompanyPaymentMethodSettings
        settings_obj, created = CompanyPaymentMethodSettings.objects.get_or_create(company=company)
        
        if request.method == "GET":
            serializer = CompanyPaymentMethodSettingsSerializer(settings_obj, context={"request": request})
            return Response(serializer.data)
            
        elif request.method == "PATCH":
            serializer = CompanyPaymentMethodSettingsSerializer(
                settings_obj, data=request.data, partial=True, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
