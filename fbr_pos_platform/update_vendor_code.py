#!/usr/bin/env python
"""
Script to update vendor_code for an existing sale.
Usage: python update_vendor_code.py <sale_id> <vendor_code>
Example: python update_vendor_code.py 9 "VENDOR-123"
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from pos.models import Sale

def update_vendor_code():
    if len(sys.argv) != 3:
        print("Usage: python update_vendor_code.py <sale_id> <vendor_code>")
        print("Example: python update_vendor_code.py 9 \"VENDOR-123\"")
        sys.exit(1)
    
    sale_id = sys.argv[1]
    vendor_code = sys.argv[2]
    
    try:
        sale = Sale.objects.get(id=sale_id)
        sale.vendor_code = vendor_code
        sale.save(update_fields=['vendor_code', 'updated_at'])
        print(f"✓ Successfully updated vendor_code for sale {sale.sale_number} to '{vendor_code}'")
        print(f"  Invoice #: {sale.sale_number}")
        print(f"  Customer: {sale.customer.name if sale.customer else 'N/A'}")
    except Sale.DoesNotExist:
        print(f"✗ Sale with ID {sale_id} not found")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    update_vendor_code()
