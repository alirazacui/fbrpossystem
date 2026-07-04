from django.db import models
from django.utils.translation import gettext_lazy as _


class PlatformSettings(models.Model):
	"""Singleton platform configuration for branding and SMTP."""

	name = models.CharField(max_length=100, default="default", unique=True)
	primary_color = models.CharField(max_length=32, default="#0f766e")
	secondary_color = models.CharField(max_length=32, default="#f8fafc")
	accent_color = models.CharField(max_length=32, default="#14b8a6")

	smtp_host = models.CharField(max_length=255, blank=True, default="")
	smtp_port = models.PositiveIntegerField(default=587)
	smtp_use_tls = models.BooleanField(default=True)
	smtp_username = models.CharField(max_length=255, blank=True, default="")
	smtp_password = models.CharField(max_length=255, blank=True, default="")
	default_from_email = models.EmailField(blank=True, default="")
	reply_to_email = models.EmailField(blank=True, default="")

	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = _("Platform Settings")
		verbose_name_plural = _("Platform Settings")

	def save(self, *args, **kwargs):
		self.name = "default"
		super().save(*args, **kwargs)

	@classmethod
	def load(cls):
		obj, _ = cls.objects.get_or_create(name="default")
		return obj
