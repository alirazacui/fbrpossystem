from rest_framework import serializers
from .models import Lead, Notification


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for Lead model - handles form submissions from landing page"""
    
    class Meta:
        model = Lead
        fields = [
            'id',
            'lead_type',
            'business_name',
            'contact_name',
            'email',
            'phone',
            'cnic',
            'address',
            'message',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new leads from public forms"""
    
    class Meta:
        model = Lead
        fields = [
            'lead_type',
            'business_name',
            'contact_name',
            'email',
            'phone',
            'cnic',
            'address',
            'message',
        ]
    
    def validate(self, data):
        lead_type = data.get('lead_type')
        
        # For business automation, CNIC is required
        if lead_type == 'business_automation' and not data.get('cnic'):
            raise serializers.ValidationError({
                'cnic': 'CNIC is required for business automation requests'
            })
        
        return data


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    lead_business_name = serializers.CharField(source='related_lead.business_name', read_only=True, allow_null=True)
    lead_type = serializers.CharField(source='related_lead.lead_type', read_only=True, allow_null=True)
    
    class Meta:
        model = Notification
        fields = [
            'id',
            'notification_type',
            'title',
            'message',
            'related_lead',
            'lead_business_name',
            'lead_type',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification read status"""
    
    class Meta:
        model = Notification
        fields = ['is_read']
