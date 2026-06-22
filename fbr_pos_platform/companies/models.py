from django.db import models

# Create your models here.
"""
companies/models.py

Company is the tenant record. Every client business that buys a POS or
Digital Invoicing licence from us gets one Company record. All non-platform
users (Owner, Manager, Cashier, Salesperson) belong to exactly one Company.

Platform users (Admin, Admin Staff) do NOT belong to any Company — they
belong to our own organisation.

Build order note
----------------
Company has NO FK to User. The circular-dependency problem is avoided by
letting User hold the FK to Company (nullable for platform users). "Who is
the owner" is determined by querying User where role='owner' and company=this.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------------------------
# Choices — defined as classes so they are importable elsewhere cleanly
# ---------------------------------------------------------------------------

class BusinessMode(models.TextChoices):
    """
    What product(s) has this company purchased from us?
    POS and Digital Invoicing are kept separate because FBR treats them as
    two different integration types even though both eventually get a QR code.
    """
    POS_ONLY  = "pos_only",  _("POS Only")
    DI_ONLY   = "di_only",   _("Digital Invoicing Only")
    BOTH      = "both",      _("POS + Digital Invoicing")


class FBRBusinessNature(models.TextChoices):
    """
    FBR's own classification of what the business *does*.
    Multiple values can apply to one company — stored as an ArrayField.
    """
    MANUFACTURER     = "manufacturer",     _("Manufacturer")
    IMPORTER         = "importer",         _("Importer")
    EXPORTER         = "exporter",         _("Exporter")
    DISTRIBUTOR      = "distributor",      _("Distributor")
    WHOLESALER       = "wholesaler",       _("Wholesaler")
    RETAILER         = "retailer",         _("Retailer")
    SERVICE_PROVIDER = "service_provider", _("Service Provider")
    OTHER            = "other",            _("Other")


class FBRSector(models.TextChoices):
    """
    FBR's sector classification — exactly ONE value per company.
    This, combined with Business Nature, determines which sandbox scenarios
    FBR assigns to this taxpayer inside IRIS.
    """
    POTASSIUM_CHLORIDE   = "potassium_chloride",   _("Potassium Chloride")
    CEMENT_CONCRETE      = "cement_concrete",       _("Cement & Concrete Block")
    MOBILE_WHOLESALE     = "mobile_wholesale",      _("Mobile Wholesale/Retail")
    PHARMACEUTICALS      = "pharmaceuticals",       _("Pharmaceuticals")
    CNG_STATION          = "cng_station",           _("CNG Station")
    AUTOMOBILES          = "automobiles",           _("Automobiles")
    SERVICES             = "services",              _("Services")
    GAS_DISTRIBUTION     = "gas_distribution",      _("Gas Distribution")
    ELECTRICITY          = "electricity",           _("Electricity Distribution")
    PETROLEUM            = "petroleum",             _("Petroleum")
    TELECOM              = "telecom",               _("Telecom")
    TEXTILE              = "textile",               _("Textile")
    FMCG                 = "fmcg",                  _("FMCG")
    STEEL                = "steel",                 _("Steel")
    ALL_OTHER            = "all_other",             _("All Other Sectors")


class BusinessVertical(models.TextChoices):
    """
    Our own internal classification — drives which POS features / UI we show.
    Completely independent of FBR Sector.

    Examples: restaurant mode enables table/floor-map features;
              grocery mode enables weight-based pricing, etc.
    """
    GROCERY        = "grocery",        _("Grocery Store")
    GENERAL_STORE  = "general_store",  _("General Store")
    RESTAURANT     = "restaurant",     _("Restaurant / F&B")
    PHARMACY       = "pharmacy",       _("Pharmacy")
    ELECTRONICS    = "electronics",    _("Electronics")
    CLOTHING       = "clothing",       _("Clothing / Apparel")
    WHOLESALE      = "wholesale",      _("Wholesale")
    OTHER          = "other",          _("Other")


class SubscriptionPlan(models.TextChoices):
    TRIAL     = "trial",     _("Trial")
    STARTER   = "starter",   _("Starter")
    PRO       = "pro",       _("Pro")
    PREMIUM   = "premium",   _("Premium")


class SubscriptionStatus(models.TextChoices):
    ACTIVE    = "active",    _("Active")
    TRIAL     = "trial",     _("Trial")
    EXPIRED   = "expired",   _("Expired")
    SUSPENDED = "suspended", _("Suspended")
    CANCELLED = "cancelled", _("Cancelled")


# ---------------------------------------------------------------------------
# Main model
# ---------------------------------------------------------------------------

class Company(models.Model):
    """
    One row = one client business (tenant).

    Sections
    --------
    1. Core business identity
    2. FBR / regulatory info
    3. Business classification (our own)
    4. Contact & branding
    5. Subscription
    6. Feature modules (hard ceiling for user permissions)
    7. FBR sandbox / onboarding state
    8. Internal admin metadata
    9. Timestamps & status
    """

    # ------------------------------------------------------------------
    # 1. Core business identity
    # ------------------------------------------------------------------

    business_name = models.CharField(
        max_length=255,
        verbose_name=_("Business Name"),
    )

    ntn = models.CharField(
        max_length=15,
        unique=True,
        verbose_name=_("NTN"),
        help_text=_("National Tax Number — 7 digits (e.g. 1234567)"),
    )

    strn = models.CharField(
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        verbose_name=_("STRN"),
        help_text=_("Sales Tax Registration Number — 13 digits"),
    )

    owner_cnic = models.CharField(
        max_length=15,
        verbose_name=_("Owner CNIC"),
        help_text=_("Format: 00000-0000000-0 (13 digits with dashes)"),
    )

    # ------------------------------------------------------------------
    # 2. FBR / regulatory info
    # ------------------------------------------------------------------

    business_mode = models.CharField(
        max_length=20,
        choices=BusinessMode.choices,
        default=BusinessMode.POS_ONLY,
        verbose_name=_("Business Mode"),
        help_text=_(
            "Which product(s) this company has licensed. "
            "Does NOT auto-set any modules — admin configures modules independently."
        ),
    )

    fbr_business_nature = ArrayField(
        base_field=models.CharField(
            max_length=30,
            choices=FBRBusinessNature.choices,
        ),
        default=list,
        blank=True,
        verbose_name=_("FBR Business Nature"),
        help_text=_("Multiple values allowed. Drives sandbox scenario assignment in IRIS."),
    )

    fbr_sector = models.CharField(
        max_length=30,
        choices=FBRSector.choices,
        blank=True,
        null=True,
        verbose_name=_("FBR Sector"),
        help_text=_("Exactly one sector. Combined with Business Nature to determine eligible scenarios."),
    )

    # ------------------------------------------------------------------
    # 3. Business classification (our own, independent of FBR)
    # ------------------------------------------------------------------

    vertical = models.CharField(
        max_length=30,
        choices=BusinessVertical.choices,
        default=BusinessVertical.GENERAL_STORE,
        verbose_name=_("Business Vertical"),
        help_text=_(
            "Internal classification that controls which POS features/UI "
            "this company sees. Independent of FBR Sector."
        ),
    )

    # ------------------------------------------------------------------
    # 4. Contact & branding
    # ------------------------------------------------------------------

    logo = models.ImageField(
        upload_to="company_logos/",
        blank=True,
        null=True,
        verbose_name=_("Company Logo"),
    )

    address = models.TextField(
        verbose_name=_("Business Address"),
        help_text=_("Full address in a single field (city, province, postal code)."),
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Business Phone"),
    )

    email = models.EmailField(
        blank=True,
        verbose_name=_("Business Email"),
    )

    website_url = models.URLField(
        blank=True,
        verbose_name=_("Website URL"),
    )

    # ------------------------------------------------------------------
    # 5. Subscription
    # ------------------------------------------------------------------

    subscription_plan = models.CharField(
        max_length=20,
        choices=SubscriptionPlan.choices,
        default=SubscriptionPlan.TRIAL,
        verbose_name=_("Subscription Plan"),
    )

    subscription_status = models.CharField(
        max_length=20,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.TRIAL,
        verbose_name=_("Subscription Status"),
    )

    subscription_start_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Subscription Start Date"),
    )

    subscription_expiry_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Subscription Expiry Date"),
    )

    next_billing_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Next Billing Date"),
    )

    # ------------------------------------------------------------------
    # 6. Feature modules — hard ceiling for all users in this company
    #
    #    Rule: a user permission can NEVER exceed what is enabled here.
    #    Admin (platform) bypasses this ceiling entirely.
    #    Owner gets everything that IS enabled here, automatically.
    # ------------------------------------------------------------------

    # --- Sales & FBR ---
    module_sales_invoicing       = models.BooleanField(default=False, verbose_name=_("Sales Invoicing"))
    module_fbr_di                = models.BooleanField(default=False, verbose_name=_("FBR Digital Invoicing"))
    module_customer_db           = models.BooleanField(default=True,  verbose_name=_("Customer Database"))  # cannot be disabled per FBR rules
    module_fbr_registered_buyer  = models.BooleanField(default=False, verbose_name=_("FBR Registered Buyer Scenarios"))

    # --- Operations ---
    module_returns               = models.BooleanField(default=False, verbose_name=_("Returns & Debit/Credit Notes"))
    module_fbr_amendments        = models.BooleanField(default=False, verbose_name=_("Manual FBR Amendments"))
    module_cheque_bank_transfer  = models.BooleanField(default=False, verbose_name=_("Cheque & Bank Transfer"))
    module_customer_display      = models.BooleanField(default=False, verbose_name=_("Customer-Facing Display"))
    module_hardware_integration  = models.BooleanField(default=False, verbose_name=_("Hardware Integration"))

    # --- Inventory ---
    module_inventory             = models.BooleanField(default=False, verbose_name=_("Inventory Tracking"))
    module_warehousing           = models.BooleanField(default=False, verbose_name=_("Warehousing"))

    # --- Multi-location (reserved — not wired to any logic yet) ---
    module_multi_location        = models.BooleanField(
        default=False,
        verbose_name=_("Multi-Location / Multi-Branch"),
        help_text=_("Reserved for future use. Currently disabled in all business logic."),
    )

    # --- Restaurant / F&B ---
    module_restaurant_fnb        = models.BooleanField(default=False, verbose_name=_("Restaurant F&B"))
    module_dine_in               = models.BooleanField(default=False, verbose_name=_("Dine-In"))
    module_takeaway              = models.BooleanField(default=False, verbose_name=_("Takeaway"))
    module_delivery              = models.BooleanField(default=False, verbose_name=_("Delivery"))
    module_table_floor_map       = models.BooleanField(default=False, verbose_name=_("Table & Floor Map"))
    module_kitchen_display       = models.BooleanField(default=False, verbose_name=_("Kitchen Display / KDS"))

    # --- Insights ---
    module_basic_reports         = models.BooleanField(default=True,  verbose_name=_("Basic Reports"))
    module_advanced_reports      = models.BooleanField(default=False, verbose_name=_("Advanced Reports"))
    module_audit_logs            = models.BooleanField(default=False, verbose_name=_("Audit Logs"))

    # ------------------------------------------------------------------
    # 7. FBR sandbox / onboarding state
    # ------------------------------------------------------------------

    fbr_sandbox_token = models.TextField(
        blank=True,
        verbose_name=_("FBR Sandbox Token"),
        help_text=_("Issued by IRIS after IP whitelisting is accepted. Used for test invoice submission."),
    )

    fbr_production_token = models.TextField(
        blank=True,
        verbose_name=_("FBR Production Token"),
        help_text=_(
            "Issued automatically by IRIS once all sandbox scenarios are cleared. "
            "Required before any live invoice can be submitted."
        ),
    )

    fbr_assigned_scenarios = ArrayField(
        base_field=models.CharField(max_length=10),
        default=list,
        blank=True,
        verbose_name=_("FBR Assigned Sandbox Scenarios"),
        help_text=_(
            "List of scenario codes this tenant must clear in sandbox "
            "(e.g. ['SN001', 'SN002', 'SN005']). "
            "Copied manually from IRIS — FBR does not expose an API for this. "
            "Admin can override the platform's auto-suggested default."
        ),
    )

    fbr_test_buyer_ntn = models.CharField(
        max_length=15,
        blank=True,
        verbose_name=_("FBR Test Buyer NTN"),
        help_text=_(
            "Required only if this tenant's scenarios include SN001 or SN005 "
            "(registered buyer scenarios). PRAL's own test NTN is NOT pre-registered."
        ),
    )

    fbr_sandbox_complete = models.BooleanField(
        default=False,
        verbose_name=_("Sandbox Testing Complete"),
        help_text=_("Flipped to True once all assigned scenarios are cleared and a production token is issued."),
    )

    # IP whitelisting (up to 3 IPs per FBR's limit)
    fbr_ip_1 = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("Whitelisted IP 1"))
    fbr_ip_2 = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("Whitelisted IP 2"))
    fbr_ip_3 = models.GenericIPAddressField(blank=True, null=True, verbose_name=_("Whitelisted IP 3"))

    # CRM credentials (for raising support cases with PRAL's DI CRM)
    fbr_crm_user_id = models.EmailField(
        blank=True,
        verbose_name=_("FBR CRM User ID (Email)"),
        help_text=_("Email registered as Technical Contact Person in IRIS Technical Details."),
    )

    # ------------------------------------------------------------------
    # 8. Internal admin metadata
    # ------------------------------------------------------------------

    account_manager = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Account Manager"),
        help_text=_("Name of the internal staff member responsible for this account."),
    )

    internal_notes = models.TextField(
        blank=True,
        verbose_name=_("Internal Notes"),
        help_text=_("Visible only to Admin/Admin Staff. Never shown in the POS or client-facing UI."),
    )

    tags = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        verbose_name=_("Tags"),
        help_text=_("Free-form labels for filtering/searching companies in the admin app."),
    )

    # ------------------------------------------------------------------
    # 9. Timestamps & status
    # ------------------------------------------------------------------

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_(
            "Inactive companies cannot log into the POS. "
            "Deactivate instead of deleting — records are never hard-deleted."
        ),
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True,     verbose_name=_("Updated At"))

    # ------------------------------------------------------------------
    # Meta & dunder
    # ------------------------------------------------------------------

    class Meta:
        verbose_name        = _("Company")
        verbose_name_plural = _("Companies")
        ordering            = ["-created_at"]
        indexes = [
            models.Index(fields=["ntn"],          name="company_ntn_idx"),
            models.Index(fields=["is_active"],    name="company_active_idx"),
            models.Index(fields=["subscription_status"], name="company_sub_status_idx"),
        ]

    def __str__(self):
        return f"{self.business_name} ({self.ntn})"

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def owner(self):
        """
        Returns the single Owner user for this company.
        Avoids a circular import by using a lazy string reference.
        Returns None if no owner has been created yet.
        """
        from users.models import User  # local import — avoids circular import at module level
        return User.objects.filter(company=self, role=User.Role.OWNER).first()

    @property
    def is_subscription_active(self):
        """Quick check used by permission classes to gate API access."""
        return self.subscription_status in (
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.TRIAL,
        )

    def get_enabled_modules(self) -> list[str]:
        """
        Returns a list of module field names that are currently True.
        Used by the permission system to validate user permission grants
        against the company ceiling.

        Example return value:
            ['module_sales_invoicing', 'module_customer_db', 'module_basic_reports']
        """
        module_fields = [f.name for f in self._meta.get_fields() if f.name.startswith("module_")]
        return [name for name in module_fields if getattr(self, name) is True]