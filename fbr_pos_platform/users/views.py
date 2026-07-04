from django.shortcuts import render

# Create your views here.
import hashlib
import secrets
from datetime import timedelta

from django.conf import settings
from django.core import signing
from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
 
from common.permissions import (
    IsAdmin,
    IsAdminOrAdminStaff,
    IsOwner,
    IsOwnerOrAdmin,
    IsActiveUser,
)
from .models import User, UserStatus
from .models import PasswordResetOTP
from .serializers import (
    ChangePasswordSerializer,
    CreateAdminStaffSerializer,
    CreateClientUserSerializer,
    CreateOwnerSerializer,
    UpdateUserStatusSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from common.email_service import send_platform_email


def _hash_otp(otp: str) -> str:
    return hashlib.sha256(f"{otp}:{settings.SECRET_KEY}".encode("utf-8")).hexdigest()
 
 
class AdminStaffViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Platform Admin manages Admin Staff users.
 
    list     GET  /api/admin-users/
    create   POST /api/admin-users/
    retrieve GET  /api/admin-users/{id}/
    update   PUT  /api/admin-users/{id}/
    delete   DELETE /api/admin-users/{id}/
    status   PATCH /api/admin-users/{id}/status/
    """
    permission_classes = [IsAdmin]
 
    def get_queryset(self):
        return User.objects.filter(
            role__in=[User.Role.ADMIN, User.Role.ADMIN_STAFF]
        ).order_by("-date_joined")
 
    def get_serializer_class(self):
        if self.action == "create":
            return CreateAdminStaffSerializer
        if self.action == "status":
            return UpdateUserStatusSerializer
        if self.action == "list":
            return UserListSerializer
        return UserDetailSerializer
 
    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):
        """PATCH /api/admin-users/{id}/status/"""
        user       = self.get_object()
        serializer = UpdateUserStatusSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserDetailSerializer(user).data)
 
 
class AllUsersViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """
    Platform Admin view to list and manage ALL users in the system.
    
    list     GET  /api/users/
    retrieve GET  /api/users/{id}/
    delete   DELETE /api/users/{id}/
    status   PATCH /api/users/{id}/status/
    """
    permission_classes = [IsAdmin]
    queryset = User.objects.all().order_by("-date_joined")
    
    def get_serializer_class(self):
        if self.action == "status":
            return UpdateUserStatusSerializer
        if self.action == "list":
            return UserListSerializer
        return UserDetailSerializer
        
    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):
        """PATCH /api/users/{id}/status/"""
        user       = self.get_object()
        serializer = UpdateUserStatusSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserDetailSerializer(user).data)
 
 
class OwnerViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    Platform Admin creates and manages Owner users.
    On creation, signal auto-grants all company-module permissions.
 
    list     GET  /api/owners/
    create   POST /api/owners/
    retrieve GET  /api/owners/{id}/
    status   PATCH /api/owners/{id}/status/
    """
    permission_classes = [IsAdmin]
 
    def get_queryset(self):
        return User.objects.filter(role=User.Role.OWNER).order_by("-date_joined")
 
    def get_serializer_class(self):
        if self.action == "create":
            return CreateOwnerSerializer
        if self.action == "status":
            return UpdateUserStatusSerializer
        if self.action == "list":
            return UserListSerializer
        return UserDetailSerializer
 
    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):
        """PATCH /api/owners/{id}/status/"""
        user       = self.get_object()
        serializer = UpdateUserStatusSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserDetailSerializer(user).data)
 
 
class CompanyUserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """
    Owner manages their own company's users (Manager, Cashier, Salesperson).
    All queries are automatically scoped to the requesting owner's company.
 
    list     GET  /api/company-users/
    create   POST /api/company-users/
    retrieve GET  /api/company-users/{id}/
    status   PATCH /api/company-users/{id}/status/
    """
    permission_classes = [IsOwner]
 
    def get_queryset(self):
        return User.objects.filter(
            company  = self.request.user.company,
            role__in = [
                User.Role.MANAGER,
                User.Role.CASHIER,
                User.Role.SALESPERSON,
            ],
        ).order_by("-date_joined")
 
    def get_serializer_class(self):
        if self.action == "create":
            return CreateClientUserSerializer
        if self.action == "status":
            return UpdateUserStatusSerializer
        if self.action == "list":
            return UserListSerializer
        return UserDetailSerializer
    def perform_create(self, serializer):
        """Check subscription user limit before creating staff user."""
        sub = getattr(self.request, "subscription", None)
        if sub:
            can_add, reason = sub.check_user_limit()
            if not can_add:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(detail=reason)
        serializer.save()
 
    @action(detail=True, methods=["patch"], url_path="status")
    def status(self, request, pk=None):
        """PATCH /api/company-users/{id}/status/"""
        user = self.get_object()
        serializer = UpdateUserStatusSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserDetailSerializer(user).data)
 
 
class MeViewSet(GenericViewSet):
    """
    Current authenticated user — profile and password.
 
    me          GET   /api/me/
    update_me   PATCH /api/me/update/
    password    POST  /api/me/password/
    """
    permission_classes = [IsActiveUser]
 
    def get_object(self):
        return self.request.user
 
    @action(detail=False, methods=["get"], url_path="")
    def me(self, request):
        """GET /api/me/"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
 
    @action(detail=False, methods=["patch"], url_path="update")
    def update_me(self, request):
        """PATCH /api/me/update/"""
        serializer = UserDetailSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
 
    @action(detail=False, methods=["post"], url_path="password")
    def password(self, request):
        """POST /api/me/password/"""
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password updated successfully."})


class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        if not email:
            return Response({"email": "Email is required."}, status=400)

        try:
            user = User.objects.get(email=email, role__in=[User.Role.OWNER, User.Role.MANAGER, User.Role.CASHIER, User.Role.SALESPERSON])
        except User.DoesNotExist:
            return Response({"detail": "If the email exists, an OTP has been sent."})

        otp = f"{secrets.randbelow(900000) + 100000}"
        PasswordResetOTP.objects.filter(email=email, used=False).update(used=True)
        record = PasswordResetOTP.objects.create(
            email=email,
            user=user,
            otp_hash=_hash_otp(otp),
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        company_login_url = getattr(settings, "FRONTEND_COMPANY_LOGIN_URL", "http://localhost:5173/login/company")
        body = (
            f"Your password reset code is: {otp}\n\n"
            f"This code expires in 10 minutes.\n"
            f"Use the company login page: {company_login_url}"
        )
        send_platform_email("Password Reset OTP", body, [email])
        return Response({"detail": "OTP sent successfully.", "request_id": signing.dumps({"otp_id": record.id})})


class PasswordResetVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = (request.data.get("email") or "").strip().lower()
        otp = (request.data.get("otp") or "").strip()
        if not email or not otp:
            return Response({"detail": "Email and OTP are required."}, status=400)

        record = PasswordResetOTP.objects.filter(email=email, used=False, verified=False).order_by("-created_at").first()
        if not record or record.expires_at < timezone.now() or record.otp_hash != _hash_otp(otp):
            return Response({"detail": "Invalid or expired OTP."}, status=400)

        record.verified = True
        record.verified_at = timezone.now()
        record.save(update_fields=["verified", "verified_at"])
        reset_token = signing.dumps({"otp_id": record.id}, salt="password-reset")
        return Response({"detail": "OTP verified.", "reset_token": reset_token})


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        reset_token = request.data.get("reset_token") or ""
        new_password = request.data.get("new_password") or ""
        confirm_password = request.data.get("confirm_password") or ""

        if not reset_token or not new_password or not confirm_password:
            return Response({"detail": "reset_token, new_password and confirm_password are required."}, status=400)
        if new_password != confirm_password:
            return Response({"confirm_password": "Passwords do not match."}, status=400)

        try:
            payload = signing.loads(reset_token, salt="password-reset", max_age=600)
        except signing.BadSignature:
            return Response({"detail": "Invalid or expired reset token."}, status=400)

        record = PasswordResetOTP.objects.filter(id=payload.get("otp_id"), used=False, verified=True).select_related("user").first()
        if not record or record.expires_at < timezone.now():
            return Response({"detail": "Reset token expired."}, status=400)

        user = record.user
        user.set_password(new_password)
        user.save(update_fields=["password", "username", "is_active", "updated_at"])
        record.used = True
        record.used_at = timezone.now()
        record.save(update_fields=["used", "used_at"])
        return Response({"detail": "Password updated successfully."})