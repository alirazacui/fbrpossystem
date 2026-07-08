"""
users/serializers.py
"""

from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.db import IntegrityError, transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.email_service import build_welcome_email_html, send_platform_email
from common.tasks import send_platform_email_task
from .models import User, UserStatus
from companies.models import Terminal


# ---------------------------------------------------------------------------
# JWT — custom claims
# ---------------------------------------------------------------------------

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Adds role, company_id, and status into the JWT payload so that
    DRF permission classes can read them from the token without an
    extra database hit on every request.

    Payload example:
        {
            "user_id": 42,
            "email": "owner@abcstore.com",
            "role": "owner",
            "company_id": 7,
            "status": "active"
        }
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"]      = user.email
        token["role"]       = user.role
        token["company_id"] = user.company_id   # None for platform users
        token["status"]     = user.status
        terminal_id = getattr(user, "terminal_id", None)
        token["terminal_id"] = str(terminal_id) if terminal_id is not None else None
        return token

    def validate(self, attrs):
        """
        Block login for inactive or suspended users BEFORE issuing a token.
        Django's default only checks is_active; we also check our status field.
        """
        email_field = self.username_field
        if email_field in attrs and isinstance(attrs[email_field], str):
            attrs[email_field] = attrs[email_field].strip().lower()

        data = super().validate(attrs)

        user = self.user
        if user.status == UserStatus.INACTIVE:
            raise serializers.ValidationError(
                "This account has been deactivated. Contact your administrator."
            )
        if user.status == UserStatus.SUSPENDED:
            raise serializers.ValidationError(
                "This account has been suspended. Contact the platform administrator."
            )

        # Add user info to the login response alongside the tokens
        data["user"] = {
            "id":         user.id,
            "email":      user.email,
            "full_name":  user.get_full_name(),
            "role":       user.role,
            "company_id": user.company_id,
            "terminal_id": str(getattr(user, "terminal_id", None)) if getattr(user, "terminal_id", None) is not None else None,
            "status":     user.status,
        }
        return data


# ---------------------------------------------------------------------------
# User serializers
# ---------------------------------------------------------------------------

class UserListSerializer(serializers.ModelSerializer):
    """
    Lightweight — for lists and dropdowns.
    """
    full_name    = serializers.CharField(source="get_full_name", read_only=True)
    company_name = serializers.CharField(
        source="company.business_name", read_only=True, default=None
    )
    terminal_id = serializers.CharField(read_only=True, default=None)
    terminal_name = serializers.CharField(source="terminal.name", read_only=True, default=None)

    class Meta:
        model  = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "status",
            "company_id",
            "company_name",
            "terminal_id",
            "terminal_name",
            "date_joined",
        ]
        read_only_fields = fields


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Full detail — for retrieve and update (no password here).
    Email and role are read-only to prevent accidental changes.
    """
    full_name    = serializers.CharField(source="get_full_name", read_only=True)
    company_name = serializers.CharField(
        source="company.business_name", read_only=True, default=None
    )
    company_id = serializers.IntegerField(
        source="company.id", read_only=True, default=None
    )
    company_ntn = serializers.CharField(
        source="company.ntn", read_only=True, default=None
    )
    terminal_id = serializers.CharField(read_only=True, default=None)
    terminal_name = serializers.CharField(source="terminal.name", read_only=True, default=None)
    created_by_email = serializers.EmailField(
        source="created_by.email", read_only=True, default=None
    )

    class Meta:
        model  = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone",
            "role",
            "status",
            "company",
            "company_id",
            "company_name",
            "company_ntn",
            "terminal_id",
            "terminal_name",
            "created_by",
            "created_by_email",
            "date_joined",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "email",
            "role",
            "full_name",
            "company_id",
            "company_name",
            "company_ntn",
            "created_by",
            "created_by_email",
            "date_joined",
            "updated_at",
        ]


class CreateAdminStaffSerializer(serializers.ModelSerializer):
    """
    Admin creates Admin Staff.
    No company field — platform users never belong to a company.
    Password is set manually by the creator.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model  = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if isinstance(attrs.get("email"), str):
            attrs["email"] = attrs["email"].strip().lower()

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        if User.objects.filter(email=value.strip().lower()).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.strip().lower()

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        request = self.context.get("request")
        try:
            user = User.objects.create_user(
                email      = validated_data["email"],
                password   = validated_data["password"],
                first_name = validated_data.get("first_name", ""),
                last_name  = validated_data.get("last_name", ""),
                phone      = validated_data.get("phone", ""),
                role       = User.Role.ADMIN_STAFF,
                status     = UserStatus.ACTIVE,
                created_by = request.user if request else None,
            )
        except IntegrityError:
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        return user


class CreateOwnerSerializer(serializers.ModelSerializer):
    """
    Admin creates an Owner for a specific Company.
    Once saved, the signal auto-grants all company-module permissions.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )

    class Meta:
        model  = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "company",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if isinstance(attrs.get("email"), str):
            attrs["email"] = attrs["email"].strip().lower()

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        cleaned = value.strip().lower()
        if User.objects.filter(email__iexact=cleaned).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return cleaned

    def validate_company(self, company):
        """
        Reject if the company already has an owner
        OR if the company is inactive.
        """
        from users.models import User as UserModel
        if not company.is_active:
            raise serializers.ValidationError(
                f"Company '{company.business_name}' is inactive. Activate it first."
            )
        if UserModel.objects.filter(company=company, role=User.Role.OWNER).exists():
            raise serializers.ValidationError(
                f"Company '{company.business_name}' already has an owner."
            )
        return company

    @transaction.atomic
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        request = self.context.get("request")
        user = User.objects.create_user(
            email      = validated_data["email"],
            password   = validated_data["password"],
            first_name = validated_data.get("first_name", ""),
            last_name  = validated_data.get("last_name", ""),
            phone      = validated_data.get("phone", ""),
            role       = User.Role.OWNER,
            company    = validated_data["company"],
            status     = UserStatus.ACTIVE,
            created_by = request.user if request else None,
        )
        company_login_url = getattr(settings, "FRONTEND_COMPANY_LOGIN_URL", "https://myfbrpos.com/login/company")
        html_body = build_welcome_email_html(
            brand_name=getattr(settings, "PLATFORM_BRAND_NAME", "FBR POS"),
            logo_path=getattr(settings, "PLATFORM_BRAND_LOGO_PATH", "") or None,
            logo_url=getattr(settings, "PLATFORM_BRAND_LOGO_URL", "") or None,
            logo_cid="brand-logo",
            recipient_name=user.get_full_name() or user.email,
            login_url=company_login_url,
            username=user.email,
            password=validated_data["password"],
            welcome_note=(
                f"Welcome to {getattr(settings, 'PLATFORM_BRAND_NAME', 'FBR POS')}. "
                "Your tenant is now active and your invoices, sales, and digital invoicing workspaces are ready."
            ),
        )
        email_subject = f"Welcome to {user.company.business_name}"
        email_body = (
            f"Hello {user.get_full_name() or user.email},\n\n"
            f"Your company owner account has been created for {user.company.business_name}.\n"
            f"Login link: {company_login_url}\n\n"
            f"Username: {user.email}\n"
            f"Password: {validated_data['password']}\n\n"
            "Please change your password after the first login."
        )
        transaction.on_commit(
            lambda: send_platform_email_task.delay(
                email_subject,
                email_body,
                [user.email],
                html_body=html_body,
                inline_image_path=getattr(settings, "PLATFORM_BRAND_LOGO_PATH", "") or None,
            )
        )
        # Signal auto_grant_owner_permissions fires here automatically
        return user


class CreateClientUserSerializer(serializers.ModelSerializer):
    """
    Owner creates Manager / Cashier / Salesperson inside their own company.
    The company is taken from the requesting owner — never from the request body.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    role = serializers.ChoiceField(
        choices=[
            User.Role.MANAGER,
            User.Role.CASHIER,
            User.Role.SALESPERSON,
        ]
    )
    terminal = serializers.PrimaryKeyRelatedField(
        queryset=Terminal.objects.select_related("company", "branch").all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model  = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
            "role",
            "terminal",
            "password",
            "confirm_password",
        ]

    def validate(self, attrs):
        if isinstance(attrs.get("email"), str):
            attrs["email"] = attrs["email"].strip().lower()

        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        request = self.context.get("request")
        if not request or not request.user or not request.user.company_id:
            raise serializers.ValidationError({"company": "Owner company is required to create company users."})

        role = attrs.get("role")
        terminal = attrs.get("terminal")

        if role in (User.Role.MANAGER, User.Role.CASHIER) and terminal is None:
            raise serializers.ValidationError({"terminal": "Terminal is required for managers and cashiers."})

        if terminal is not None and request and request.user.company_id and terminal.company_id != request.user.company_id:
            raise serializers.ValidationError({"terminal": "Terminal must belong to your company."})

        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        request = self.context.get("request")
        owner_company = getattr(request.user, "company", None) if request else None
        if owner_company is None:
            raise serializers.ValidationError({"company": "Owner company is required to create company users."})

        # Company comes from the requesting owner — not from the payload
        user = User.objects.create_user(
            email      = validated_data["email"],
            password   = validated_data["password"],
            first_name = validated_data.get("first_name", ""),
            last_name  = validated_data.get("last_name", ""),
            phone      = validated_data.get("phone", ""),
            role       = validated_data["role"],
            company    = owner_company,
            terminal   = validated_data.get("terminal"),
            status     = UserStatus.ACTIVE,
            created_by = request.user,
        )
        return user


class UpdateUserStatusSerializer(serializers.ModelSerializer):
    """
    Dedicated serializer just for changing a user's status.
    Keeps status changes as an explicit separate action.
    """

    class Meta:
        model  = User
        fields = ["status"]

    def validate_status(self, value):
        request = self.context.get("request")
        target  = self.instance

        # Only platform Admin can suspend or un-suspend
        if value == UserStatus.SUSPENDED:
            if not request.user.is_platform_admin:
                raise serializers.ValidationError(
                    "Only platform Admin can suspend a user."
                )

        # Owner cannot reactivate a suspended user
        if (
            target.status == UserStatus.SUSPENDED
            and value == UserStatus.ACTIVE
            and not request.user.is_platform_admin
        ):
            raise serializers.ValidationError(
                "Only platform Admin can lift a suspension."
            )

        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Allows a user to change their own password.
    """
    old_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={"input_type": "password"},
    )
    confirm_new_password = serializers.CharField(
        write_only=True,
        style={"input_type": "password"},
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_new_password"]:
            raise serializers.ValidationError(
                {"confirm_new_password": "New passwords do not match."}
            )
        return attrs

    def save(self):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user