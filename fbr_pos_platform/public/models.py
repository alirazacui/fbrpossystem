from django.db import models
from django.utils import timezone


class Lead(models.Model):
    """
    Stores lead submissions from landing page forms.
    Two types: 'demo_request' (Book Demo) and 'business_automation' (Automate Business)
    """
    LEAD_TYPE_CHOICES = [
        ('demo_request', 'Demo Request'),
        ('business_automation', 'Business Automation'),
    ]
    
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    ]
    
    lead_type = models.CharField(max_length=50, choices=LEAD_TYPE_CHOICES)
    business_name = models.CharField(max_length=255)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cnic = models.CharField(max_length=15, blank=True, null=True, help_text="For business automation requests")
    address = models.TextField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        return f"{self.business_name} - {self.get_lead_type_display()}"


class Notification(models.Model):
    """
    Admin notifications for various events including lead submissions.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('lead_submission', 'Lead Submission'),
        ('system_alert', 'System Alert'),
        ('subscription', 'Subscription'),
        ('support', 'Support Request'),
    ]
    
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_lead = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
