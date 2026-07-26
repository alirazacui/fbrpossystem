"""
companies/pos_settings_serializer.py

Serializer for POS FBR Settings page.
Client enters their POS credentials here after login.
"""

from rest_framework import serializers
from .models import Company


class POSFBRSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for POS FBR settings page.
    
    Client enters their POS credentials here:
    - POS ID (from FBR registration)
    - Access Code
    - Sandbox Token
    - Production Token
    
    These fields are separate from DI credentials.
    """
    
    class Meta:
        model = Company
        fields = [
            "pos_id",
            "pos_access_code",
            "pos_sandbox_token",
            "pos_production_token",
            "pos_sandbox_endpoint",
            "pos_production_endpoint",
        ]
    
    def validate_pos_id(self, value):
        """POS ID must be numeric."""
        if value and not value.isdigit():
            raise serializers.ValidationError("POS ID must be numeric.")
        return value
    
    def validate(self, attrs):
        """
        Validate that at least POS ID and Access Code are provided.
        """
        pos_id = attrs.get("pos_id")
        access_code = attrs.get("pos_access_code")
        
        if not pos_id or not access_code:
            raise serializers.ValidationError(
                "POS ID and Access Code are required."
            )
        
        return attrs
