from django.urls import path
from .views import AdminDashboardStatsView, AdminFbrTokensView, AdminFbrTokenDetailView, AdminInvoicesView, AdminInvoiceDocumentView, AdminAuditLogsView, AdminAuditLogDetailView, PlatformSettingsView, AdminPasswordChangeView

urlpatterns = [
    path('admin-dashboard/stats/', AdminDashboardStatsView.as_view(), name='admin-dashboard-stats'),
    path('admin-dashboard/fbr-tokens/', AdminFbrTokensView.as_view(), name='admin-dashboard-fbr-tokens'),
    path('admin-dashboard/fbr-tokens/<str:token_id>/', AdminFbrTokenDetailView.as_view(), name='admin-dashboard-fbr-token-detail'),
    path('admin-dashboard/invoices/', AdminInvoicesView.as_view(), name='admin-dashboard-invoices'),
    path('admin-dashboard/invoices/<int:sale_id>/document/', AdminInvoiceDocumentView.as_view(), name='admin-dashboard-invoice-document'),
    path('admin-dashboard/audit-logs/', AdminAuditLogsView.as_view(), name='admin-dashboard-audit-logs'),
    path('admin-dashboard/audit-logs/<str:log_id>/', AdminAuditLogDetailView.as_view(), name='admin-dashboard-audit-log-detail'),
    path('platform-settings/', PlatformSettingsView.as_view(), name='platform-settings'),
    path('platform-settings/change-password/', AdminPasswordChangeView.as_view(), name='platform-settings-change-password'),
]
