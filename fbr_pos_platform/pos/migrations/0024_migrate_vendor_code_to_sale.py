from django.db import migrations

def migrate_vendor_code_to_sale(apps, schema_editor):
    """
    Copy vendor_code from Customer to Sale for all existing sales.
    This ensures historical invoices retain their vendor codes.
    """
    Sale = apps.get_model('pos', 'Sale')
    Customer = apps.get_model('pos', 'Customer')
    
    # Get all sales with customers that have vendor codes
    sales_with_vendor = Sale.objects.select_related('customer').filter(
        customer__vendor_code__isnull=False
    ).exclude(customer__vendor_code='').exclude(customer__vendor_code='0')
    
    count = 0
    for sale in sales_with_vendor:
        if sale.customer.vendor_code and sale.customer.vendor_code != "0":
            sale.vendor_code = sale.customer.vendor_code
            sale.save(update_fields=['vendor_code'])
            count += 1
    
    print(f"Migrated vendor_code for {count} sales")

class Migration(migrations.Migration):
    dependencies = [
        ('pos', '0023_sale_vendor_code'),  # The migration that added vendor_code to Sale
    ]
    
    operations = [
        migrations.RunPython(migrate_vendor_code_to_sale),
    ]
