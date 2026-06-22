from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Company
 
 
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
 
    # ── List view ──────────────────────────────────────────────────────
    list_display = [
        "business_name",
        "ntn",
        "vertical",
        "business_mode",
        "subscription_plan",
        "subscription_status",
        "is_active",
        "logo_preview",
        "created_at",
    ]
    list_filter  = [
        "is_active",
        "business_mode",
        "vertical",
        "subscription_plan",
        "subscription_status",
        "fbr_sector",
    ]
    search_fields = ["business_name", "ntn", "strn", "owner_cnic", "email"]
    ordering      = ["-created_at"]
    readonly_fields = [
        "created_at",
        "updated_at",
        "logo_preview",
        "owner_info",
        "enabled_modules_display",
    ]
 
    # ── Detail view — organised into sections ──────────────────────────
    fieldsets = (
        ("Core Business Identity", {
            "fields": (
                "business_name",
                "ntn",
                "strn",
                "owner_cnic",
                "owner_info",
            )
        }),
        ("FBR / Regulatory", {
            "fields": (
                "business_mode",
                "fbr_business_nature",
                "fbr_sector",
            )
        }),
        ("Our Classification", {
            "fields": ("vertical",)
        }),
        ("Contact & Branding", {
            "fields": (
                "logo",
                "logo_preview",
                "address",
                "phone",
                "email",
                "website_url",
            )
        }),
        ("Subscription", {
            "fields": (
                "subscription_plan",
                "subscription_status",
                "subscription_start_date",
                "subscription_expiry_date",
                "next_billing_date",
            )
        }),
        ("Feature Modules", {
            "classes": ("collapse",),
            "fields": (
                "enabled_modules_display",
                # Sales & FBR
                "module_sales_invoicing",
                "module_fbr_di",
                "module_customer_db",
                "module_fbr_registered_buyer",
                # Operations
                "module_returns",
                "module_fbr_amendments",
                "module_cheque_bank_transfer",
                "module_customer_display",
                "module_hardware_integration",
                # Inventory
                "module_inventory",
                "module_warehousing",
                "module_multi_location",
                # Restaurant
                "module_restaurant_fnb",
                "module_dine_in",
                "module_takeaway",
                "module_delivery",
                "module_table_floor_map",
                "module_kitchen_display",
                # Insights
                "module_basic_reports",
                "module_advanced_reports",
                "module_audit_logs",
            )
        }),
        ("FBR Sandbox / Onboarding", {
            "classes": ("collapse",),
            "fields": (
                "fbr_sandbox_token",
                "fbr_production_token",
                "fbr_assigned_scenarios",
                "fbr_test_buyer_ntn",
                "fbr_sandbox_complete",
                "fbr_ip_1",
                "fbr_ip_2",
                "fbr_ip_3",
                "fbr_crm_user_id",
            )
        }),
        ("Internal Admin Metadata", {
            "classes": ("collapse",),
            "fields": (
                "account_manager",
                "internal_notes",
                "tags",
            )
        }),
        ("Status & Timestamps", {
            "fields": (
                "is_active",
                "created_at",
                "updated_at",
            )
        }),
    )
 
    # ── Custom display methods ─────────────────────────────────────────
 
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:40px; border-radius:4px;" />',
                obj.logo.url
            )
        return "—"
    logo_preview.short_description = "Logo"
 
    def owner_info(self, obj):
        owner = obj.owner
        if owner:
            return format_html(
                "<strong>{}</strong> &lt;{}&gt;",
                owner.get_full_name() or "—",
                owner.email,
            )
        return format_html(
    '<span style="color:{};">{}</span>',
    'orange',
    '⚠ No owner assigned yet'
)
    owner_info.short_description = "Current Owner"
 
    def enabled_modules_display(self, obj):
        modules = obj.get_enabled_modules()
        if not modules:
            return "No modules enabled"
        items = "".join(
            f'<li style="color:green;">✓ {m.replace("module_", "").replace("_", " ").title()}</li>'
            for m in modules
        )
        return format_html(
    "<ul style='margin:0;padding-left:16px;'>{}</ul>",
    items,
)
    enabled_modules_display.short_description = "Enabled Modules"