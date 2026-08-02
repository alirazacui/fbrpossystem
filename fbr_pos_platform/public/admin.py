from django.contrib import admin
from .models import Lead, Notification


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['business_name', 'lead_type', 'email', 'phone', 'status', 'created_at']
    list_filter = ['lead_type', 'status', 'created_at']
    search_fields = ['business_name', 'email', 'phone', 'contact_name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Lead Information', {
            'fields': ('lead_type', 'business_name', 'contact_name', 'status')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'cnic', 'address')
        }),
        ('Additional Information', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Notification Details', {
            'fields': ('notification_type', 'title', 'message', 'is_read')
        }),
        ('Related Lead', {
            'fields': ('related_lead',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
