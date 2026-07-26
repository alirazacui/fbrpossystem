"""
========================================================
digital_invoicing/pos_invoice_builder.py

FBR Retail POS Invoice JSON Builder

Assembles the complete FBR POS invoice JSON from a Sale object.
This is the bridge between our Django models and the FBR POS API payload.

FBR POS invoice JSON structure:
{
    "POSID": 123456,
    "USIN": "INV-2025-000001",
    "DateTime": "2025-01-15T10:30:00",
    "BuyerName": "Customer Name",
    "BuyerPNTN": "1234567-8",
    "BuyerCNIC": "1234567890123",
    "BuyerPhoneNumber": "03001234567",
    "TotalSaleValue": 1000.00,
    "TotalTaxCharged": 180.00,
    "Discount": 0,
    "FurtherTax": 0,
    "TotalBillAmount": 1180.00,
    "PaymentMode": 1,
    "InvoiceType": 1,
    "Items": [
        {
            "ItemCode": "IT_1011",
            "ItemName": "Product Name",
            "PCTCode": "11001010",
            "Quantity": 2.0,
            "TaxRate": 18,
            "SaleValue": 1000.00,
            "Discount": 0,
            "FurtherTax": 0,
            "TaxCharged": 180.00,
            "TotalAmount": 1180.00,
            "InvoiceType": 1
        }
    ]
}
========================================================
"""

from django.utils import timezone


class POSInvoiceBuilder:
    """
    Builds the complete FBR POS invoice JSON payload from a Sale instance.

    Usage:
        builder = POSInvoiceBuilder(sale)
        payload = builder.build()
        # payload is ready to POST to FBR POS API
    """

    def __init__(self, sale):
        self.sale = sale
        self.company = sale.company
        self.customer = sale.customer

    def build(self) -> dict:
        """
        Assembles and returns the complete FBR POS invoice JSON dict.
        """
        payload = {
            # ── Header ───────────────────────────────────────────────
            "POSID": int(self.company.pos_id) if self.company.pos_id else 0,
            "USIN": self._generate_pos_usin(),
            "DateTime": self._format_datetime(self.sale.completed_at),
            
            # ── Buyer (customer) ──────────────────────────────────────
            "BuyerName": self.customer.name or "Walk-In Customer",
            "BuyerPNTN": self._extract_ntn(self.customer.ntn_cnic),
            "BuyerCNIC": self._extract_cnic(self.customer.ntn_cnic),
            "BuyerPhoneNumber": self.customer.phone or "",
            
            # ── Totals ───────────────────────────────────────────────
            "TotalSaleValue": float(self.sale.subtotal),
            "TotalQuantity": float(sum(line.quantity for line in self.sale.lines.all())),
            "TotalTaxCharged": float(self.sale.total_tax),
            "Discount": float(self.sale.total_discount),
            "FurtherTax": float(self.sale.total_further_tax),
            "TotalBillAmount": float(self.sale.total_amount),
            
            # ── Payment & Invoice Type ────────────────────────────────
            "PaymentMode": self._determine_payment_mode(),
            "RefInvoiceNumber": None,  # For credit/debit notes, reference original invoice
            "InvoiceType": self._determine_invoice_type(),
            
            # ── Items ─────────────────────────────────────────────────
            "Items": self._build_items(),
        }
        return payload

    def _generate_pos_usin(self) -> str:
        """
        Generate POS-specific USIN format.
        Format: {BRANCH_CODE}-{TERMINAL_CODE}-{YEAR}-{SEQUENCE}
        Example: PT-MAIN-T1-2026-0000010
        """
        from django.utils import timezone
        
        year = timezone.now().year
        
        # Get branch code (first 2-3 letters of branch name, uppercase)
        branch_code = "PT"  # Default prefix
        if self.sale.cashier and self.sale.cashier.terminal and self.sale.cashier.terminal.branch:
            branch = self.sale.cashier.terminal.branch
            branch_code = (branch.code or branch.name[:3] or "PT").upper()
        
        # Get terminal code from cashier's terminal
        terminal_code = "T1"  # Default
        if self.sale.cashier and self.sale.cashier.terminal:
            terminal = self.sale.cashier.terminal
            # Use terminal name or index as code
            terminal_code = terminal.terminal_index or terminal.name[:10] or "T1"
            # Clean up terminal code (remove spaces, special chars)
            terminal_code = terminal_code.replace(" ", "").replace("-", "")[:10]
        
        # Get sequence number from sale_number (extract the last part)
        # sale_number format: INV-{company_id}-{year}-{sequence}
        parts = self.sale.sale_number.split("-")
        sequence = parts[-1] if len(parts) >= 4 else "000001"
        
        # Build USIN: BRANCH_CODE-TERMINAL_CODE-YEAR-SEQUENCE
        usin = f"{branch_code}-{terminal_code}-{year}-{sequence}"
        return usin

    def _format_datetime(self, dt) -> str:
        """Format datetime to FBR POS expected format: YYYY-MM-DDTHH:mm:ss.000"""
        if dt is None:
            dt = timezone.now()
        return timezone.localtime(dt).strftime("%Y-%m-%dT%H:%M:%S.000")

    def _extract_ntn(self, ntn_cnic: str) -> str:
        """
        Extract NTN from ntn_cnic field.
        NTN is 7 or 9 digits, optionally with check digit (e.g., "1234567-8").
        """
        if not ntn_cnic:
            return ""
        # NTN is 7-9 digits, CNIC is 13 digits
        core = ntn_cnic.split("-")[0].strip()
        if len(core) <= 9:
            return core
        return ""

    def _extract_cnic(self, ntn_cnic: str) -> str:
        """
        Extract CNIC from ntn_cnic field.
        CNIC is 13 digits.
        """
        if not ntn_cnic:
            return ""
        core = ntn_cnic.split("-")[0].strip()
        if len(core) == 13:
            return core
        return ""

    def _determine_payment_mode(self) -> int:
        """
        Determine payment mode from sale payments.
        1 = Cash
        2 = Card
        3 = Cheque
        4 = Bank Transfer
        5 = JazzCash
        6 = EasyPaisa
        7 = Raast
        
        If multiple payment methods, use the first one.
        """
        from pos.models import PaymentMethod
        
        if not self.sale.payments.exists():
            return 1  # Default to cash
        
        first_payment = self.sale.payments.first()
        mode_map = {
            PaymentMethod.CASH: 1,
            PaymentMethod.CARD: 2,
            PaymentMethod.CHEQUE: 3,
            PaymentMethod.BANK_TRANSFER: 4,
            PaymentMethod.JAZZCASH: 5,
            PaymentMethod.EASYPAISA: 6,
            PaymentMethod.RAAST: 7,
        }
        return mode_map.get(first_payment.payment_method, 1)

    def _determine_invoice_type(self) -> int:
        """
        Determine invoice type.
        1 = Sale Invoice
        2 = Purchase Invoice (not used in our system)
        3 = Debit Note
        4 = Credit Note
        """
        from pos.models import SaleType
        
        type_map = {
            SaleType.SALE_INVOICE: 1,
            SaleType.DEBIT_NOTE: 3,
            SaleType.CREDIT_NOTE: 4,
        }
        return type_map.get(self.sale.sale_type, 1)

    def _build_items(self) -> list:
        """Build the items array from all SaleLines."""
        return [
            self._build_item(line)
            for line in self.sale.lines.all()
        ]

    def _build_item(self, line) -> dict:
        """Build a single item dict from a SaleLine."""
        # Format PCT code: remove decimal point (2106.9090 -> 21069090)
        pct_code = line.product.pct_code or "00000000"
        pct_code = pct_code.replace(".", "")
        
        return {
            "ItemCode": line.product.sku or f"IT_{line.product.id}",
            "ItemName": line.product_name,
            "PCTCode": pct_code,
            "Quantity": float(line.quantity),
            "TaxRate": self._parse_tax_rate(line.tax_rate_percent),
            "SaleValue": float(line.value_excl_tax),
            "Discount": float(line.discount_amount),
            "FurtherTax": float(line.further_tax),
            "TaxCharged": float(line.sales_tax_applicable),
            "TotalAmount": float(line.line_total),
            "InvoiceType": self._determine_invoice_type(),
        }

    def _parse_tax_rate(self, rate_str: str) -> int:
        """
        Parse tax rate string to integer.
        "18%" -> 18
        "Exempt" -> 0
        "0%" -> 0
        """
        if not rate_str:
            return 0
        if rate_str == "Exempt":
            return 0
        # Remove % and convert to int
        rate = rate_str.replace("%", "").strip()
        try:
            return int(float(rate))
        except (ValueError, TypeError):
            return 0
