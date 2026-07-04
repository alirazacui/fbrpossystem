# Generated manually for PlatformSettings.

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='PlatformSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default', max_length=100, unique=True)),
                ('primary_color', models.CharField(default='#0f766e', max_length=32)),
                ('secondary_color', models.CharField(default='#f8fafc', max_length=32)),
                ('accent_color', models.CharField(default='#14b8a6', max_length=32)),
                ('smtp_host', models.CharField(blank=True, default='', max_length=255)),
                ('smtp_port', models.PositiveIntegerField(default=587)),
                ('smtp_use_tls', models.BooleanField(default=True)),
                ('smtp_username', models.CharField(blank=True, default='', max_length=255)),
                ('smtp_password', models.CharField(blank=True, default='', max_length=255)),
                ('default_from_email', models.EmailField(blank=True, default='', max_length=254)),
                ('reply_to_email', models.EmailField(blank=True, default='', max_length=254)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Platform Settings',
                'verbose_name_plural': 'Platform Settings',
            },
        ),
    ]