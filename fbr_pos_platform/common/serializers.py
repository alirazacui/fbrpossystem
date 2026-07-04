from rest_framework import serializers

from common.models import PlatformSettings


class PlatformSettingsSerializer(serializers.ModelSerializer):
    smtp_password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = PlatformSettings
        fields = [
            "primary_color",
            "secondary_color",
            "accent_color",
            "smtp_host",
            "smtp_port",
            "smtp_use_tls",
            "smtp_username",
            "smtp_password",
            "default_from_email",
            "reply_to_email",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        if not validated_data.get("smtp_password"):
            validated_data.pop("smtp_password", None)
        return super().update(instance, validated_data)


class AdminPasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs


class CompanyOwnerPasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs
