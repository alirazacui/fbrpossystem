"""
companies/serializers.py
"""

import base64

from django.conf import settings
from django.db import IntegrityError
from django.db import transaction
from rest_framework import serializers
from .models import Company, AuditLog, Branch, Warehouse
from .models import Company, AuditLog, Branch, Warehouse, Terminal
from common.email_service import build_welcome_email_html, send_platform_email
from common.tasks import send_platform_email_task


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'company', 'name', 'code', 'city', 'province', 'address', 'is_active', 'is_default', 'created_at']
        read_only_fields = ['id', 'company', 'created_at']


class WarehouseSerializer(serializers.ModelSerializer):
    branch_name = serializers.SerializerMethodField()

    class Meta:
        model = Warehouse
        fields = ['id', 'company', 'branch', 'branch_name', 'name', 'code', 'city', 'address', 'is_active', 'is_default', 'created_at']
        read_only_fields = ['id', 'company', 'created_at']

    def get_branch_name(self, obj):
        return obj.branch.name if obj.branch else None


class TerminalSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source="branch.name", read_only=True)
    company_name = serializers.CharField(source="company.business_name", read_only=True)

    class Meta:
        model = Terminal
        fields = [
            "id",
            "company",
            "company_name",
            "branch",
            "branch_name",
            "name",
            "device_fingerprint",
            "terminal_index",
            "pairing_code",
            "pairing_code_expires_at",
            "paired_at",
            "os_version",
            "app_version",
            "printer_config",
            "scanner_config",
            "drawer_config",
            "customer_display_enabled",
            "is_active",
            "last_seen_at",
            "last_synced_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "company",
            "company_name",
            "branch_name",
            "pairing_code",
            "pairing_code_expires_at",
            "paired_at",
            "created_at",
            "updated_at",
            "last_seen_at",
            "last_synced_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        branch = validated_data["branch"]
        validated_data["company"] = branch.company
        return super().create(validated_data)

    def update(self, instance, validated_data):
        branch = validated_data.get("branch", instance.branch)
        if branch:
            validated_data["company"] = branch.company
        return super().update(instance, validated_data)




class CompanyListSerializer(serializers.ModelSerializer):
    """
    Lightweight — used for lists and dropdowns.
    Only the fields needed to identify a company at a glance.
    """
    owner_email = serializers.SerializerMethodField()
    subscription_active = serializers.BooleanField(
        source="is_subscription_active", read_only=True
    )

    class Meta:
        model = Company
        fields = [
            "id",
            "business_name",
            "ntn",
            "vertical",
            "subscription_plan",
            "subscription_status",
            "subscription_active",
            "is_active",
            "owner_email",
            "created_at",
        ]
        read_only_fields = fields

    def get_owner_email(self, obj):
        owner = obj.owner  # uses the property on Company
        return owner.email if owner else None


class CompanyDetailSerializer(serializers.ModelSerializer):
    """
    Full detail — used for create, retrieve, update.
    Includes all fields including modules and FBR sandbox state.
    """
    tenant_owner_email = serializers.EmailField(write_only=True, required=False, allow_blank=False)
    tenant_owner_first_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tenant_owner_last_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tenant_owner_phone = serializers.CharField(write_only=True, required=False, allow_blank=True)
    tenant_owner_password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    tenant_owner_confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=False)
    owner_email = serializers.SerializerMethodField()
    owner_id    = serializers.SerializerMethodField()
    enabled_modules = serializers.ListField(
        source="get_enabled_modules", read_only=True
    )

    class Meta:
        model = Company
        fields = [
            # ── Core identity ──────────────────────────────
            "id",
            "business_name",
            "ntn",
            "strn",
            "owner_cnic",
            "tenant_owner_email",
            "tenant_owner_first_name",
            "tenant_owner_last_name",
            "tenant_owner_phone",
            "tenant_owner_password",
            "tenant_owner_confirm_password",

            # ── FBR / regulatory ───────────────────────────
            "business_mode",
            "fbr_business_nature",
            "fbr_sector",

            # ── Our own classification ─────────────────────
            "vertical",

            # ── Contact & branding ─────────────────────────
            "logo",
            "address",
            "phone",
            "email",
            "website_url",

            # ── Subscription ───────────────────────────────
            "subscription_plan",
            "subscription_status",
            "subscription_start_date",
            "subscription_expiry_date",
            "next_billing_date",

            # ── Modules ────────────────────────────────────
            "module_invoices",
            "module_fbr_di",
            "module_customer_db",
            "module_multi_branch",
            "module_terminals_cash_sessions",
            "module_user_management",
            "module_inventory",
            "module_warehousing",
            "module_returns",
            "module_debit_credit_notes",
            "module_fbr_amendments",
            "module_cheque_bank_transfer",
            "module_customer_display",
            "module_hardware_integration",
            "module_restaurant_fnb",
            "module_basic_reports",
            "module_advanced_reports",
            "module_audit_logs",
            "enabled_modules",           # computed, read-only

            # ── FBR sandbox ────────────────────────────────
            "fbr_sandbox_token",
            "fbr_production_token",
            "fbr_sandbox_endpoint",
            "fbr_production_endpoint",
            "fbr_test_buyer_ntn",
            "fbr_sandbox_complete",
            "fbr_ip_1",
            "fbr_ip_2",
            "fbr_ip_3",
            "fbr_crm_user_id",

            # ── Sandbox scenarios ──────────────────────────
            "fbr_scenario_sn001",
            "fbr_scenario_sn002",
            "fbr_scenario_sn003",
            "fbr_scenario_sn004",
            "fbr_scenario_sn005",
            "fbr_scenario_sn006",
            "fbr_scenario_sn007",
            "fbr_scenario_sn008",
            "fbr_scenario_sn009",
            "fbr_scenario_sn010",
            "fbr_scenario_sn011",
            "fbr_scenario_sn012",
            "fbr_scenario_sn013",
            "fbr_scenario_sn014",
            "fbr_scenario_sn015",
            "fbr_scenario_sn016",
            "fbr_scenario_sn017",
            "fbr_scenario_sn018",
            "fbr_scenario_sn019",
            "fbr_scenario_sn020",
            "fbr_scenario_sn021",
            "fbr_scenario_sn022",
            "fbr_scenario_sn023",
            "fbr_scenario_sn024",
            "fbr_scenario_sn025",
            "fbr_scenario_sn026",
            "fbr_scenario_sn027",
            "fbr_scenario_sn028",

            # ── Internal admin ─────────────────────────────
            "account_manager",
            "internal_notes",
            "tags",

            # ── Status & timestamps ────────────────────────
            "is_active",
            "created_at",
            "updated_at",

            # ── Computed ───────────────────────────────────
            "owner_email",
            "owner_id",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_active",
            "owner_email",
            "owner_id",
            "enabled_modules",
            "fbr_sandbox_complete",     # set by system, not manually
        ]

    def get_owner_email(self, obj):
        owner = obj.owner
        return owner.email if owner else None

    def get_owner_id(self, obj):
        owner = obj.owner
        return owner.id if owner else None

    def validate_fbr_business_nature(self, value):
        """Ensure at least one business nature is selected."""
        if not value:
            raise serializers.ValidationError(
                "At least one FBR Business Nature must be selected."
            )
        return value

    def validate_ntn(self, value):
        """NTN must be numeric digits only."""
        cleaned = value.replace("-", "").strip()
        if not cleaned.isdigit():
            raise serializers.ValidationError(
                "NTN must contain digits only (dashes are stripped automatically)."
            )
        return cleaned

    def validate_owner_cnic(self, value):
        """CNIC: strip dashes and validate 13 digits."""
        cleaned = value.replace("-", "").strip()
        if not cleaned.isdigit() or len(cleaned) != 13:
            raise serializers.ValidationError(
                "CNIC must be exactly 13 digits (format: 00000-0000000-0)."
            )
        return value  # keep original formatted value

    def validate_strn(self, value):
        """STRN is optional; blank values should be stored as NULL."""
        if value is None:
            return None
        cleaned = value.strip()
        return cleaned or None

    def validate_tenant_owner_email(self, value):
        from users.models import User

        cleaned = value.strip().lower()
        if User.objects.filter(email__iexact=cleaned).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return cleaned

    def validate_tenant_owner_password(self, value):
        return value

    def _queue_logo_upload(self, company: Company, logo_file):
        if not logo_file:
            return

        if hasattr(logo_file, "read"):
            logo_file.seek(0)
            file_bytes = logo_file.read()
        else:
            file_bytes = logo_file

        encoded_logo = base64.b64encode(file_bytes).decode("utf-8")
        original_name = getattr(logo_file, "name", "logo.png")
        content_type = getattr(logo_file, "content_type", None)

        from .tasks import upload_company_logo_to_s3

        transaction.on_commit(
            lambda: upload_company_logo_to_s3.delay(
                company_id=company.id,
                logo_base64=encoded_logo,
                filename=original_name,
                content_type=content_type,
            )
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)

        owner_fields = [
            "tenant_owner_email",
            "tenant_owner_first_name",
            "tenant_owner_last_name",
            "tenant_owner_phone",
            "tenant_owner_password",
            "tenant_owner_confirm_password",
        ]
        provided_owner_fields = [field for field in owner_fields if attrs.get(field)]

        if provided_owner_fields and len(provided_owner_fields) != len(owner_fields):
            missing_fields = [field for field in owner_fields if not attrs.get(field)]
            raise serializers.ValidationError({
                field: ["This field is required when creating a tenant owner."]
                for field in missing_fields
            })

        if attrs.get("tenant_owner_email"):
            attrs["tenant_owner_email"] = attrs["tenant_owner_email"].strip().lower()

        if attrs.get("tenant_owner_password") and attrs.get("tenant_owner_confirm_password"):
            if attrs["tenant_owner_password"] != attrs["tenant_owner_confirm_password"]:
                raise serializers.ValidationError({"tenant_owner_confirm_password": "Passwords do not match."})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        logo_file = validated_data.pop("logo", None)

        owner_email = validated_data.pop("tenant_owner_email", None)
        owner_first_name = validated_data.pop("tenant_owner_first_name", "")
        owner_last_name = validated_data.pop("tenant_owner_last_name", "")
        owner_phone = validated_data.pop("tenant_owner_phone", "")
        owner_password = validated_data.pop("tenant_owner_password", None)
        validated_data.pop("tenant_owner_confirm_password", None)

        company = super().create(validated_data)
        self._queue_logo_upload(company, logo_file)

        if owner_email:
            from users.models import User, UserStatus

            request = self.context.get("request")
            try:
                user = User.objects.create_user(
                    email=owner_email,
                    password=owner_password,
                    first_name=owner_first_name,
                    last_name=owner_last_name,
                    phone=owner_phone,
                    role=User.Role.OWNER,
                    company=company,
                    status=UserStatus.ACTIVE,
                    created_by=request.user if request else None,
                )
            except IntegrityError:
                raise serializers.ValidationError({"tenant_owner_email": "A user with this email already exists."})

            company_login_url = getattr(settings, "FRONTEND_COMPANY_LOGIN_URL", "https://myfbrpos.com/login/company")
            html_body = build_welcome_email_html(
                brand_name=getattr(settings, "PLATFORM_BRAND_NAME", "FBR POS"),
                logo_path=getattr(settings, "PLATFORM_BRAND_LOGO_PATH", "") or None,
                logo_url=getattr(settings, "PLATFORM_BRAND_LOGO_URL", "") or None,
                logo_cid="brand-logo",
                recipient_name=user.get_full_name() or user.email,
                login_url=company_login_url,
                username=user.email,
                password=owner_password,
                welcome_note=(
                    f"Welcome to {getattr(settings, 'PLATFORM_BRAND_NAME', 'FBR POS')}. "
                    "Your tenant is ready and all invoices, sales, and digital invoicing tools are available from your dashboard."
                ),
            )
            email_subject = f"Welcome to {company.business_name}"
            email_body = (
                f"Hello {user.get_full_name() or user.email},\n\n"
                f"Your company owner account has been created for {company.business_name}.\n"
                f"Login link: {company_login_url}\n\n"
                f"Username: {user.email}\n"
                f"Password: {owner_password}\n\n"
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

        return company

    @transaction.atomic
    def update(self, instance, validated_data):
        logo_file = validated_data.pop("logo", None)
        company = super().update(instance, validated_data)
        self._queue_logo_upload(company, logo_file)
        return company


class CompanyModulesSerializer(serializers.ModelSerializer):
    """
    Thin serializer just for updating a company's module toggles.
    Used by Admin when enabling/disabling features for a company.
    Separate from CompanyDetailSerializer so the endpoint is explicit
    and can't accidentally update business identity fields.
    """

    class Meta:
        model = Company
        fields = [
            "module_invoices",
            "module_fbr_di",
            "module_customer_db",
            "module_multi_branch",
            "module_terminals_cash_sessions",
            "module_user_management",
            "module_inventory",
            "module_warehousing",
            "module_returns",
            "module_debit_credit_notes",
            "module_fbr_amendments",
            "module_cheque_bank_transfer",
            "module_customer_display",
            "module_hardware_integration",
            "module_restaurant_fnb",
            "module_basic_reports",
            "module_advanced_reports",
            "module_audit_logs",
        ]


from pos.models import CompanyPaymentMethodSettings

class CompanyPaymentMethodSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPaymentMethodSettings
        fields = [
            "id",
            "is_cash_enabled",
            "is_card_enabled",
            "is_easypaisa_enabled",
            "is_jazzcash_enabled",
            "is_raast_enabled",
            "is_bank_transfer_enabled",
            "is_cheque_enabled",
            "easypaisa_merchant_id",
            "easypaisa_qr_image",
            "jazzcash_merchant_id",
            "jazzcash_qr_image",
            "raast_iban",
            "raast_qr_image",
            "bank_name",
            "bank_account_name",
            "bank_iban",
        ]

    def validate(self, attrs):
        # 1. EasyPaisa validation
        is_ep_enabled = attrs.get("is_easypaisa_enabled", self.instance.is_easypaisa_enabled if self.instance else False)
        if is_ep_enabled:
            ep_merchant = attrs.get("easypaisa_merchant_id", self.instance.easypaisa_merchant_id if self.instance else "").strip()
            ep_qr = attrs.get("easypaisa_qr_image", self.instance.easypaisa_qr_image if self.instance else None)
            if not ep_merchant or not ep_qr:
                raise serializers.ValidationError({
                    "is_easypaisa_enabled": "You must provide both Merchant ID and QR Image before enabling EasyPaisa."
                })

        # 2. JazzCash validation
        is_jc_enabled = attrs.get("is_jazzcash_enabled", self.instance.is_jazzcash_enabled if self.instance else False)
        if is_jc_enabled:
            jc_merchant = attrs.get("jazzcash_merchant_id", self.instance.jazzcash_merchant_id if self.instance else "").strip()
            jc_qr = attrs.get("jazzcash_qr_image", self.instance.jazzcash_qr_image if self.instance else None)
            if not jc_merchant or not jc_qr:
                raise serializers.ValidationError({
                    "is_jazzcash_enabled": "You must provide both Merchant ID and QR Image before enabling JazzCash."
                })

        # 3. Raast validation
        is_raast_enabled = attrs.get("is_raast_enabled", self.instance.is_raast_enabled if self.instance else False)
        if is_raast_enabled:
            raast_iban = attrs.get("raast_iban", self.instance.raast_iban if self.instance else "").strip()
            raast_qr = attrs.get("raast_qr_image", self.instance.raast_qr_image if self.instance else None)
            if not raast_iban or not raast_qr:
                raise serializers.ValidationError({
                    "is_raast_enabled": "You must provide both IBAN (receiver) and QR Image before enabling Raast."
                })

        # 4. Bank Transfer validation
        is_bank_enabled = attrs.get("is_bank_transfer_enabled", self.instance.is_bank_transfer_enabled if self.instance else False)
        if is_bank_enabled:
            bank_name = attrs.get("bank_name", self.instance.bank_name if self.instance else "").strip()
            acc_name = attrs.get("bank_account_name", self.instance.bank_account_name if self.instance else "").strip()
            iban = attrs.get("bank_iban", self.instance.bank_iban if self.instance else "").strip()
            if not bank_name or not acc_name or not iban:
                raise serializers.ValidationError({
                    "is_bank_transfer_enabled": "You must provide Bank Name, Account Name, and IBAN before enabling Bank Transfer."
                })

        return attrs