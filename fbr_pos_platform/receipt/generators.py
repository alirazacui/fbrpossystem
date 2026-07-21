"""
========================================================
receipts/generators.py
 
Two receipt generators:
  ThermalReceiptGenerator  → 80mm thermal printer format
  A4InvoiceGenerator       → Full A4 formal invoice
 
Both use reportlab and save to S3 via Django's default storage.
 
Usage:
    from receipts.generators import ThermalReceiptGenerator, A4InvoiceGenerator
 
    # Generate thermal receipt
    pdf_url = ThermalReceiptGenerator(sale).generate()
 
    # Generate A4 invoice
    pdf_url = A4InvoiceGenerator(sale).generate()
========================================================
"""
 
import io
import logging
import qrcode
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, Image,
)
from reportlab.pdfgen import canvas
from config.storage_backends import invoice_pdf_upload_path
 
logger = logging.getLogger(__name__)
 
# ── Thermal receipt dimensions ────────────────────────────────────────────────
THERMAL_WIDTH  = 80 * mm     # 80mm paper width
THERMAL_MARGIN = 4 * mm      # small margins for thermal
 
 
def _generate_qr_image(data: str, size_mm: float = 25) -> io.BytesIO:
    """
    Generates a QR code image as a BytesIO buffer.
    Used for FBR invoice QR code on receipts.
    """
    qr = qrcode.QRCode(
        version           = 1,
        error_correction  = qrcode.constants.ERROR_CORRECT_M,
        box_size          = 4,
        border            = 2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img    = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer
 
 
def _s3_path_for_receipt(sale, receipt_type: str) -> str:
    """
    Returns the S3 storage path for a receipt.
    Path: company_{id}/invoices/{year}/{month}/{sale_number}_{type}.pdf
    """
    base_path = invoice_pdf_upload_path(sale, f"{sale.sale_number}.pdf")
    if receipt_type == "a4":
        return base_path
    return base_path.replace(".pdf", f"_{receipt_type}.pdf")
 
 
# ===========================================================================
# THERMAL RECEIPT GENERATOR (80mm)
# ===========================================================================
 
class ThermalReceiptGenerator:
    """
    Generates an 80mm thermal printer receipt PDF.
 
    Layout:
    ┌────────────────────────────┐
    │     COMPANY NAME           │  ← centered, bold
    │     Address, Phone         │  ← centered, small
    │     NTN: 1234567           │
    ├────────────────────────────┤
    │  SALE INVOICE              │
    │  INV-2025-000001           │
    │  Date: 15-Jan-2025 10:30   │
    │  Cashier: ahmed@store.com  │
    │  Customer: Walk-In         │
    ├────────────────────────────┤
    │  Item Name          Qty  Total │
    │  Widget A × 2       2   472  │
    │  Widget B           1   118  │
    ├────────────────────────────┤
    │  Subtotal:          Rs. 500  │
    │  Tax (18%):         Rs. 90   │
    │  Discount:          Rs. 0    │
    │  TOTAL:             Rs. 590  │
    ├────────────────────────────┤
    │  Cash:              Rs. 600  │
    │  Change:            Rs. 10   │
    ├────────────────────────────┤
    │  FBR Invoice: 7000007DI...   │
    │  [QR CODE]                   │
    │  Thank you for shopping!     │
    └────────────────────────────┘
    """
 
    def __init__(self, sale):
        self.sale    = sale
        self.company = sale.company
        self.buffer  = io.BytesIO()
 
    def generate(self, force_regenerate: bool = False) -> str:
    
        if self.sale.receipt_thermal_url and not force_regenerate:
            return self.sale.receipt_thermal_url

        self._build_pdf()
        url = self._save_to_s3("thermal")

        from django.utils import timezone
        self.sale.receipt_thermal_url  = url
        self.sale.receipt_generated_at = timezone.now()
        self.sale.save(update_fields=[
            "receipt_thermal_url",
            "receipt_generated_at",
            "updated_at",
            ])
        return url
 
    def _build_pdf(self):
        """Builds the complete thermal receipt using reportlab canvas."""
        from reportlab.lib.pagesizes import portrait
 
        # Dynamic page height based on content
        estimated_height = self._estimate_height()
        page_size        = (THERMAL_WIDTH, estimated_height)
 
        c = canvas.Canvas(self.buffer, pagesize=page_size)
        width, height = page_size
        y             = height - THERMAL_MARGIN
 
        # ── Helper functions ───────────────────────────────────────────
        def draw_text(text, x, y_pos, font="Helvetica", size=7, align="left"):
            c.setFont(font, size)
            if align == "center":
                c.drawCentredString(width / 2, y_pos, text)
            elif align == "right":
                c.drawRightString(width - THERMAL_MARGIN, y_pos, text)
            else:
                c.drawString(x, y_pos, text)
 
        def draw_line(y_pos):
            c.setLineWidth(0.3)
            c.line(THERMAL_MARGIN, y_pos, width - THERMAL_MARGIN, y_pos)
 
        def next_line(y_pos, spacing=8):
            return y_pos - spacing
 
        # ── Company header ─────────────────────────────────────────────
        draw_text(self.company.business_name.upper(), 0, y, "Helvetica-Bold", 10, "center")
        y = next_line(y, 11)
 
        if self.company.address:
            # wrap long address
            addr = self.company.address[:45]
            draw_text(addr, 0, y, "Helvetica", 6, "center")
            y = next_line(y, 8)
 
        if self.company.phone:
            draw_text(f"Tel: {self.company.phone}", 0, y, "Helvetica", 6, "center")
            y = next_line(y, 8)
 
        draw_text(f"NTN: {self.company.ntn}", 0, y, "Helvetica", 6, "center")
        y = next_line(y, 8)
 
        if self.company.strn:
            draw_text(f"STRN: {self.company.strn}", 0, y, "Helvetica", 6, "center")
            y = next_line(y, 8)
 
        # ── Separator ──────────────────────────────────────────────────
        draw_line(y)
        y = next_line(y, 6)
 
        # ── Invoice info ───────────────────────────────────────────────
        draw_text(self.sale.sale_type.upper(), 0, y, "Helvetica-Bold", 8, "center")
        y = next_line(y, 10)
 
        draw_text(f"Invoice #: {self.sale.sale_number}", THERMAL_MARGIN, y, size=7)
        y = next_line(y)
 
        completed = timezone.localtime(self.sale.completed_at) if self.sale.completed_at else timezone.localtime(timezone.now())
        draw_text(
            f"Date: {completed.strftime('%d-%b-%Y %I:%M %p')}",
            THERMAL_MARGIN, y, size=7
        )
        y = next_line(y)
 
        draw_text(
            f"Cashier: {self.sale.cashier.get_full_name() or self.sale.cashier.email}",
            THERMAL_MARGIN, y, size=7
        )
        y = next_line(y)
 
        # ── Customer / Bill-To ────────────────────────────────────────
        cust       = self.sale.customer
        cust_name  = getattr(cust, 'name', '') or ''
        cust_ntn   = getattr(cust, 'ntn_cnic', '') or ''
        cust_email = getattr(cust, 'email', '') or ''
        cust_addr  = getattr(cust, 'address', '') or ''
        is_walkin  = (
            not cust_name
            or cust_name.strip().lower() in ('walk-in', 'walkin', 'walk in', 'anonymous', 'cash customer', '-')
        )

        draw_line(y)
        y = next_line(y, 6)
        draw_text("BILL TO", 0, y, "Helvetica-Bold", 7, "center")
        y = next_line(y, 9)

        if is_walkin:
            draw_text("Walk-in Customer", THERMAL_MARGIN, y, "Helvetica-Bold", 7)
            y = next_line(y)
        else:
            if cust_name:
                draw_text(cust_name, THERMAL_MARGIN, y, "Helvetica-Bold", 7)
                y = next_line(y)
            if cust_ntn:
                draw_text(f"NTN/CNIC: {cust_ntn}", THERMAL_MARGIN, y, size=6)
                y = next_line(y, 8)
            if cust_email:
                draw_text(f"Email: {cust_email}", THERMAL_MARGIN, y, size=6)
                y = next_line(y, 8)
            if cust_addr:
                # wrap long address
                addr_line = cust_addr[:42]
                draw_text(f"Addr: {addr_line}", THERMAL_MARGIN, y, size=6)
                y = next_line(y, 8)
 
        # ── Separator ──────────────────────────────────────────────────
        draw_line(y)
        y = next_line(y, 6)
 
        # ── Column headers ─────────────────────────────────────────────
        c.setFont("Helvetica-Bold", 7)
        c.drawString(THERMAL_MARGIN, y, "Item")
        c.drawRightString(width - THERMAL_MARGIN, y, "Amount")
        y = next_line(y, 3)
        draw_line(y)
        y = next_line(y, 6)
 
        # ── Line items ─────────────────────────────────────────────────
        for line in self.sale.lines.all():
            c.setFont("Helvetica", 7)
            # Product name (truncate if too long)
            name = line.product_name[:28]
            c.drawString(THERMAL_MARGIN, y, name)
            y = next_line(y, 8)
 
            # Qty × price = total
            detail = (
                f"  {line.quantity} × Rs.{line.unit_price}"
                f"  Tax: Rs.{line.sales_tax_applicable}"
            )
            c.setFont("Helvetica", 6)
            c.drawString(THERMAL_MARGIN, y, detail)
            c.setFont("Helvetica-Bold", 7)
            c.drawRightString(
                width - THERMAL_MARGIN, y,
                f"Rs. {line.line_total:.2f}"
            )
            y = next_line(y, 9)
 
        # ── Separator ──────────────────────────────────────────────────
        draw_line(y)
        y = next_line(y, 6)
 
        # ── Totals ─────────────────────────────────────────────────────
        def draw_total_row(label, value, bold=False):
            nonlocal y
            font = "Helvetica-Bold" if bold else "Helvetica"
            size = 8 if bold else 7
            c.setFont(font, size)
            c.drawString(THERMAL_MARGIN, y, label)
            c.drawRightString(width - THERMAL_MARGIN, y, f"Rs. {value:.2f}")
            y = next_line(y, 9 if bold else 8)
 
        draw_total_row("Subtotal:", float(self.sale.subtotal))
        if float(self.sale.total_discount) > 0:
            draw_total_row("Discount:", float(self.sale.total_discount))
        draw_total_row("Sales Tax:", float(self.sale.total_tax))
        if float(self.sale.total_fed) > 0:
            draw_total_row("FED:", float(self.sale.total_fed))
 
        draw_line(y)
        y = next_line(y, 4)
        draw_total_row("TOTAL:", float(self.sale.total_amount), bold=True)
        draw_line(y)
        y = next_line(y, 6)
 
        # ── Payment breakdown ──────────────────────────────────────────
        for payment in self.sale.payments.all():
            draw_total_row(
                f"{payment.get_payment_method_display()}:",
                float(payment.amount)
            )
 
        if float(self.sale.change_given) > 0:
            draw_total_row("Change:", float(self.sale.change_given))
 
        # ── FBR section ────────────────────────────────────────────────
        if self.sale.fbr_invoice_number:
            y = next_line(y, 4)
            draw_line(y)
            y = next_line(y, 6)
 
            draw_text("FBR VERIFIED INVOICE", 0, y, "Helvetica-Bold", 7, "center")
            y = next_line(y, 9)
 
            # Wrap long FBR invoice number
            fbr_no = self.sale.fbr_invoice_number
            if len(fbr_no) > 30:
                draw_text(fbr_no[:30], 0, y, "Helvetica", 6, "center")
                y = next_line(y, 8)
                draw_text(fbr_no[30:], 0, y, "Helvetica", 6, "center")
                y = next_line(y, 8)
            else:
                draw_text(fbr_no, 0, y, "Helvetica", 6, "center")
                y = next_line(y, 8)
 
            # QR Code
            if self.sale.fbr_qr_code:
                qr_buffer = _generate_qr_image(self.sale.fbr_qr_code, 25)
                qr_size   = 25 * mm
                qr_x      = (width - qr_size) / 2
                y        -= qr_size
                c.drawImage(
                    qr_buffer, qr_x, y,
                    width=qr_size, height=qr_size,
                )
                y = next_line(y, 4)
 
        # ── Footer ─────────────────────────────────────────────────────
        draw_line(y)
        y = next_line(y, 6)
        draw_text("Thank you for your business!", 0, y, "Helvetica", 7, "center")
        y = next_line(y, 8)
        draw_text(
            completed.strftime("Printed: %d-%b-%Y %I:%M %p"),
            0, y, "Helvetica", 6, "center"
        )
 
        c.save()
 
    def _estimate_height(self) -> float:
        """Estimates page height based on number of lines."""
        base_height  = 185 * mm   # extra room for BILL TO section
        lines_height = self.sale.lines.count() * 17 * mm
        qr_height    = 30 * mm if self.sale.fbr_qr_code else 0
        return base_height + lines_height + qr_height
 
    def _save_to_s3(self, receipt_type: str) -> str:
        """Saves PDF buffer to S3 and returns URL."""
        self.buffer.seek(0)
        path = _s3_path_for_receipt(self.sale, receipt_type)
        saved_path = default_storage.save(path, ContentFile(self.buffer.read()))
        return default_storage.url(saved_path)
 
 
# ===========================================================================
# A4 INVOICE GENERATOR
# ===========================================================================
 
class A4InvoiceGenerator:
    """
    Generates a full A4 formal invoice PDF.
 
    Layout:
    ┌──────────────────────────────────────────┐
    │  [LOGO]          SALES INVOICE           │
    │  Company Name    Invoice #: INV-2025-001 │
    │  Address         Date: 15-Jan-2025       │
    │  NTN / STRN      Status: PAID            │
    ├──────────────────────────────────────────┤
    │  BILL TO:                                │
    │  Customer Name   NTN/CNIC: 1234567       │
    │  Address         Type: Registered        │
    ├──────────────────────────────────────────┤
    │  # │ Description │ Qty │ Price │ Tax │ Total │
    │  1 │ Widget A    │  2  │ 200  │ 36 │  236  │
    ├──────────────────────────────────────────┤
    │                  Subtotal:    Rs. 400    │
    │                  Sales Tax:   Rs. 72     │
    │                  Discount:    Rs. 0      │
    │                  TOTAL:       Rs. 472    │
    ├──────────────────────────────────────────┤
    │  Payment: Cash Rs. 500  Change: Rs. 28   │
    ├──────────────────────────────────────────┤
    │  FBR Invoice Number: 7000007DI...        │
    │  [QR CODE]    Scenario: SN002            │
    └──────────────────────────────────────────┘
    """
 
    # Brand colors - Matching the reference invoice style
    PRIMARY_COLOR   = colors.HexColor("#0f3d64")   # Dark blue for company name
    SECONDARY_COLOR = colors.HexColor("#f8f9fa")   # Light gray
    TEXT_COLOR      = colors.HexColor("#333333")   # Dark gray/black
    MUTED_COLOR     = colors.HexColor("#888888")   # Gray
    ACCENT_COLOR    = colors.HexColor("#00a651")   # Green for FBR and borders
 
    def __init__(self, sale):
        self.sale    = sale
        self.company = sale.company
        self.buffer  = io.BytesIO()
 
    def generate(self, force_regenerate: bool = False) -> str:
        """
        Generates the A4 invoice PDF and saves to S3.
        Returns the S3 URL.
        """
        if self.sale.receipt_a4_url and not force_regenerate:
            return self.sale.receipt_a4_url

        self._build_pdf()
        url = self._save_to_s3("a4")
        self.sale.receipt_a4_url = url
        self.sale.receipt_generated_at = timezone.now()
        self.sale.save(update_fields=["receipt_a4_url", "receipt_generated_at", "updated_at"])
        return url
 
    def _build_pdf(self):
        """Builds the A4 invoice using reportlab Platypus."""
        # Custom page template for a full-page border
        def _page_border(canvas, doc):
            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor("#dde3ea"))
            canvas.setLineWidth(1)
            # A4 is 210x297 mm. Margins are 15mm.
            canvas.rect(15 * mm, 15 * mm, A4[0] - 30 * mm, A4[1] - 30 * mm)
            canvas.restoreState()

        doc = SimpleDocTemplate(
            self.buffer,
            pagesize       = A4,
            rightMargin    = 15 * mm,
            leftMargin     = 15 * mm,
            topMargin      = 15 * mm,
            bottomMargin   = 15 * mm,
        )

        styles = getSampleStyleSheet()
        story  = []
        width  = A4[0] - 30 * mm   # usable width = 180 mm

        # ── Unified brand palette (navy primary, green only for FBR status) ──
        NAV   = self.PRIMARY_COLOR          # #0f3d64
        TXT   = self.TEXT_COLOR             # #333333
        MUT   = self.MUTED_COLOR            # #888888
        GRN   = self.ACCENT_COLOR           # #00a651
        LGRAY = colors.HexColor("#f0f4f8")  # slightly darker background for visibility
        MGRAY = colors.HexColor("#c8d8e8")  # darker border

        # ── Utility: clean stray trailing digits & title-case ─────────
        import re as _re
        def _clean(text):
            t = (_re.sub(r'\d+$', '', (text or '').strip())).strip()
            return t.title() if t else (text or '')

        # ── Utility: quick Paragraph factory ──────────────────────────
        def _p(text, size=8, bold=False, color=None, align=TA_LEFT, leading=None):
            return Paragraph(text, ParagraphStyle(
                f"_dyn_{size}_{bold}_{id(text)}",
                fontSize=size,
                fontName="Helvetica-Bold" if bold else "Helvetica",
                textColor=color or TXT,
                alignment=align,
                leading=leading or (size + 3),
            ))

        # ── Utility: panel content generator ──────────────────────────
        def _get_panel_content(rows, col_w, lbl, lbl_color=NAV, inner_padding=8):
            label_p = Paragraph(lbl, ParagraphStyle(
                "PanelLbl", fontSize=7, fontName="Helvetica-Bold",
                textColor=lbl_color, spaceAfter=5,
            ))
            inner = Table(rows, colWidths=[col_w * 0.35, col_w * 0.65])
            inner.setStyle(TableStyle([
                ("FONTSIZE",      (0, 0), (-1, -1), 8),
                ("TEXTCOLOR",     (0, 0), (0,  -1), MUT),
                ("TEXTCOLOR",     (1, 0), (1,  -1), TXT),
                ("TOPPADDING",    (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("LEFTPADDING",   (0, 0), (-1, -1), 0),
            ]))
            return [label_p, inner]

        completed = (
            timezone.localtime(self.sale.completed_at)
            if self.sale.completed_at
            else timezone.localtime(timezone.now())
        )

        # ══════════════════════════════════════════════════════════════
        # 1.  TOP NAVY BAR (full width inside margin)
        # ══════════════════════════════════════════════════════════════
        story.append(HRFlowable(
            width="100%", thickness=5, color=NAV,
            spaceAfter=5 * mm, spaceBefore=0,
        ))

        # ══════════════════════════════════════════════════════════════
        # 2.  HEADER: Logo | Business Name | Invoice Meta Box
        # ══════════════════════════════════════════════════════════════
        # A) Logo
        logo_cell = []
        try:
            from django.conf import settings as _cfg
            _lp = str(_cfg.BASE_DIR / "static_assets" / "fbr_digital_invoice.png")
            logo_cell.append(Image(_lp, width=34 * mm, height=26 * mm))
        except Exception:
            logo_cell.append(_p("<b>FBR DIGITAL<br/>INVOICING</b>", 8, color=GRN))

        # B) Business Name Hero
        hero_cell = [
            _p(f"<b>{self.company.business_name.upper()}</b>", 18, bold=True, color=NAV, leading=20),
            Spacer(1, 2 * mm),
            _p("SALES INVOICE", 10, bold=True, color=MUT, leading=12),
        ]

        # C) Meta Box (Bordered panel)
        validated = bool(self.sale.fbr_invoice_number)
        status_txt   = "FBR VALIDATED" if validated else "PENDING SUBMISSION"
        status_color = GRN if validated else MUT

        meta_rows = [
            [_p("Invoice #", 8, color=MUT), _p(f"<b>{self.sale.sale_number}</b>", 9, color=NAV)],
            [_p("Date", 8, color=MUT), _p(completed.strftime('%d %b %Y'), 8)],
        ]
        if validated:
            meta_rows.append([_p("FBR Inv", 8, color=MUT), _p(f"<b>{self.sale.fbr_invoice_number}</b>", 7, color=GRN)])
        meta_rows.append([_p("Status", 8, color=MUT), _p(f"● {status_txt}", 7, bold=True, color=status_color)])

        meta_table = Table(meta_rows, colWidths=[width * 0.15, width * 0.25])
        meta_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 2),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))

        hdr = Table(
            [[logo_cell, hero_cell, meta_table]],
            colWidths=[width * 0.20, width * 0.40, width * 0.40],
        )
        hdr.setStyle(TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("ALIGN",        (2, 0), (2,  0),  "RIGHT"),
        ]))
        story.append(hdr)
        story.append(Spacer(1, 6 * mm))

        # ══════════════════════════════════════════════════════════════
        # 3.  SELLER  |  BUYER  — equal bordered panels
        # ══════════════════════════════════════════════════════════════
        half = (width - 4 * mm) / 2

        seller_rows = []
        if self.company.address:
            seller_rows.append([_p("Address", 8, color=MUT), _p(self.company.address.title(), 8)])
        if getattr(self.company, 'phone', None):
            seller_rows.append([_p("Phone", 8, color=MUT), _p(self.company.phone, 8)])
        seller_rows.append([_p("NTN", 8, color=MUT), _p(f"<b>{self.company.ntn}</b>", 8, bold=True)])
        if getattr(self.company, 'strn', None) and self.company.strn:
            seller_rows.append([_p("STRN", 8, color=MUT), _p(self.company.strn, 8)])

        customer  = self.sale.customer
        cust_name = getattr(customer, 'name', '') or ''
        cust_ntn  = getattr(customer, 'ntn_cnic', '') or ''
        cust_mail = getattr(customer, 'email', '') or ''
        cust_addr = getattr(customer, 'address', '') or ''
        cust_reg  = getattr(customer, 'registration_type', '') or ''
        is_walkin = (
            not cust_name
            or cust_name.strip().lower() in
               ('walk-in', 'walkin', 'walk in', 'anonymous', 'cash customer', '-')
        )

        if is_walkin:
            buyer_rows = [
                [_p("Customer", 8, color=MUT), _p("<b>Walk-in Customer</b>", 9, bold=True, color=NAV)],
                [_p("", 8), _p("No registered account", 8, color=MUT)],
            ]
        else:
            buyer_rows = [
                [_p("Customer", 8, color=MUT), _p(f"<b>{cust_name}</b>", 9, bold=True, color=NAV)],
            ]
            if cust_ntn:
                buyer_rows.append([_p("NTN / CNIC", 8, color=MUT), _p(f"<b>{cust_ntn}</b>", 8, bold=True)])
            if cust_mail:
                buyer_rows.append([_p("Email", 8, color=MUT), _p(cust_mail, 8)])
            if cust_addr:
                buyer_rows.append([_p("Address", 8, color=MUT), _p(cust_addr.title(), 8)])
            if cust_reg:
                buyer_rows.append([_p("Type", 8, color=MUT), _p(str(cust_reg).replace('_', ' ').title(), 8)])

        gutter = 4 * mm
        half = (width - gutter) / 2

        parties = Table(
            [[
                _get_panel_content(seller_rows, half, "FROM — SELLER"),
                "",
                _get_panel_content(buyer_rows, half, "BILL TO — BUYER")
            ]],
            colWidths=[half, gutter, half],
        )
        parties.setStyle(TableStyle([
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
            
            # Seller Box (Col 0)
            ("BACKGROUND",   (0, 0), (0, 0), LGRAY),
            ("BOX",          (0, 0), (0, 0), 0.5, MGRAY),
            ("LINEABOVE",    (0, 0), (0, 0), 2, NAV),
            ("LEFTPADDING",  (0, 0), (0, 0), 8),
            ("RIGHTPADDING", (0, 0), (0, 0), 8),
            ("TOPPADDING",   (0, 0), (0, 0), 8),
            ("BOTTOMPADDING",(0, 0), (0, 0), 8),
            
            # Spacer (Col 1) - no styling needed, just empty
            
            # Buyer Box (Col 2)
            ("BACKGROUND",   (2, 0), (2, 0), LGRAY),
            ("BOX",          (2, 0), (2, 0), 0.5, MGRAY),
            ("LINEABOVE",    (2, 0), (2, 0), 2, NAV),
            ("LEFTPADDING",  (2, 0), (2, 0), 8),
            ("RIGHTPADDING", (2, 0), (2, 0), 8),
            ("TOPPADDING",   (2, 0), (2, 0), 8),
            ("BOTTOMPADDING",(2, 0), (2, 0), 8),
        ]))
        story.append(parties)
        story.append(Spacer(1, 5 * mm))

        # ══════════════════════════════════════════════════════════════
        # 4.  ITEMS TABLE — bordered + zebra rows
        # ══════════════════════════════════════════════════════════════
        ch  = ParagraphStyle("CH",  fontSize=8, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_LEFT)
        chr_ = ParagraphStyle("CHR", fontSize=8, fontName="Helvetica-Bold", textColor=colors.white, alignment=TA_RIGHT)
        cd  = ParagraphStyle("CD",  fontSize=8, textColor=TXT, alignment=TA_LEFT)
        cdr = ParagraphStyle("CDR", fontSize=8, textColor=TXT, alignment=TA_RIGHT)

        items_data = [[
            Paragraph("#",           ch),
            Paragraph("HS Code",     ch),
            Paragraph("Description", ch),
            Paragraph("Qty",         chr_),
            Paragraph("UoM",         ch),
            Paragraph("Rate",        chr_),
            Paragraph("Tax%",        chr_),
            Paragraph("Tax",         chr_),
            Paragraph("Amount",      chr_),
        ]]

        for idx, line in enumerate(self.sale.lines.all(), start=1):
            prod = line.product
            desc = _clean(prod.name) or prod.name
            items_data.append([
                Paragraph(f"{idx:02d}", cd),
                Paragraph(prod.hs_code or "—", cd),
                Paragraph(f"<b>{desc}</b>", cd),
                Paragraph(f"{line.quantity:g}", cdr),
                Paragraph(prod.unit_of_measure or "—", cd),
                Paragraph(f"Rs.{line.unit_price:.2f}", cdr),
                Paragraph(line.tax_rate_percent or "—", cdr),
                Paragraph(f"Rs.{line.sales_tax_applicable:.2f}", cdr),
                Paragraph(f"<b>Rs.{line.line_total:.2f}</b>", cdr),
            ])

        col_widths = [width * p for p in (0.05, 0.11, 0.26, 0.07, 0.09, 0.12, 0.07, 0.10, 0.13)]
        items_tbl = Table(items_data, colWidths=col_widths, repeatRows=1)

        it_cmds = [
            ("BACKGROUND",   (0, 0), (-1, 0),   NAV),
            ("TOPPADDING",   (0, 0), (-1, 0),   7),
            ("BOTTOMPADDING",(0, 0), (-1, 0),   7),
            ("TOPPADDING",   (0, 1), (-1, -1),  5),
            ("BOTTOMPADDING",(0, 1), (-1, -1),  5),
            ("VALIGN",       (0, 0), (-1, -1),  "MIDDLE"),
            ("BOX",          (0, 0), (-1, -1),  0.5, MGRAY),
            ("LINEBELOW",    (0, 0), (-1, -2),  0.3, MGRAY),
        ]
        for r in range(1, len(items_data)):
            if r % 2 == 0:
                it_cmds.append(("BACKGROUND", (0, r), (-1, r), LGRAY))
        items_tbl.setStyle(TableStyle(it_cmds))
        story.append(items_tbl)
        story.append(Spacer(1, 4 * mm))

        # ══════════════════════════════════════════════════════════════
        # 5.  TOTALS — right-aligned box
        # ══════════════════════════════════════════════════════════════
        def _tot(lbl, val, bold=False):
            ls = ParagraphStyle(f"TL_{id(lbl)}", fontSize=9,
                fontName="Helvetica-Bold" if bold else "Helvetica",
                alignment=TA_LEFT, textColor=NAV if bold else MUT)
            vs = ParagraphStyle(f"TV_{id(lbl)}", fontSize=9,
                fontName="Helvetica-Bold" if bold else "Helvetica",
                alignment=TA_RIGHT, textColor=NAV if bold else TXT)
            return [Paragraph(lbl, ls), Paragraph(val, vs)]

        Rs = "Rs."
        tot_rows = [_tot("Subtotal",    f"{Rs} {float(self.sale.subtotal):.2f}")]
        if float(self.sale.total_discount) > 0:
            tot_rows.append(_tot("Discount", f"- {Rs} {float(self.sale.total_discount):.2f}"))
        tot_rows.append(_tot("Sales Tax",  f"{Rs} {float(self.sale.total_tax):.2f}"))
        if float(self.sale.total_fed) > 0:
            tot_rows.append(_tot("FED Payable", f"{Rs} {float(self.sale.total_fed):.2f}"))
        grand_idx = len(tot_rows)
        tot_rows.append(_tot("GRAND TOTAL", f"{Rs} {float(self.sale.total_amount):.2f}", bold=True))
        tot_rows.append(_tot("Amount Paid",  f"{Rs} {float(self.sale.amount_paid):.2f}"))
        bal = max(0.0, float(self.sale.total_amount) - float(self.sale.amount_paid))
        tot_rows.append(_tot("Balance Due",  f"{Rs} {bal:.2f}"))

        tot_w = width * 0.40  # Totals table width is 40% of page
        tot_tbl = Table(tot_rows, colWidths=[tot_w * 0.5, tot_w * 0.5])
        tot_tbl.setStyle(TableStyle([
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
            ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
            ("TOPPADDING",    (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("BOX",           (0, 0), (-1, -1), 0.5, MGRAY),
            ("BACKGROUND",    (0, 0), (-1, -1), colors.white),
            ("LINEBELOW",     (0, 0), (-1, -4), 0.3, MGRAY),
            # grand total row
            ("BACKGROUND",    (0, grand_idx), (-1, grand_idx), LGRAY),
            ("LINEABOVE",     (0, grand_idx), (-1, grand_idx), 1.5, NAV),
            ("LINEBELOW",     (0, grand_idx), (-1, grand_idx), 1.5, NAV),
            ("FONTSIZE",      (0, grand_idx), (-1, grand_idx), 10),
            ("TOPPADDING",    (0, grand_idx), (-1, grand_idx), 7),
            ("BOTTOMPADDING", (0, grand_idx), (-1, grand_idx), 7),
        ]))

        wrapper = Table(
            [[Paragraph("", styles["Normal"]), tot_tbl]],
            colWidths=[width * 0.60, tot_w],
        )
        wrapper.setStyle(TableStyle([
            ("LEFTPADDING",  (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("VALIGN",       (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(wrapper)
        story.append(Spacer(1, 6 * mm))

        # ══════════════════════════════════════════════════════════════
        # 7.  FBR AUTHENTICATION & QR — shaded footer band
        # ══════════════════════════════════════════════════════════════
        auth = (
            f"This invoice was submitted to FBR Digital Invoicing and validated by PRAL on "
            f"<b>{completed.strftime('%d %b %Y, %H:%M')}</b>."
        )
        if self.sale.fbr_invoice_number:
            auth += f"  FBR Invoice No: <b>{self.sale.fbr_invoice_number}</b>."
        auth += (
            "  To verify, scan the QR code with the FBR <b>Tax Asaan</b> app "
            "or search at <b>e.fbr.gov.pk</b>."
        )
        disclaimer = (
            "Computer-generated invoice — no physical signature required. "
            "E&OE. Goods not returnable except per documented returns policy. "
            "Issued via FBR POS System."
        )
        
        auth_text_col = [
            _p("✔  FBR AUTHENTICATION", 8, bold=True, color=NAV),
            Spacer(1, 2 * mm),
            _p(auth, 7, color=TXT, leading=10),
            Spacer(1, 2 * mm),
            _p(disclaimer, 6, color=MUT, leading=9),
        ]
        
        if self.sale.fbr_qr_code:
            _qb2 = _generate_qr_image(self.sale.fbr_qr_code)
            qr_footer_col = [
                Image(_qb2, width=28 * mm, height=28 * mm),
                _p("SCAN TO VERIFY", 6, color=MUT, align=TA_CENTER)
            ]
            fbr_footer_content = [[auth_text_col, qr_footer_col]]
            fbr_col_widths = [width - 35 * mm, 35 * mm]
        else:
            fbr_footer_content = [[auth_text_col]]
            fbr_col_widths = [width]

        fbr_band = Table(fbr_footer_content, colWidths=fbr_col_widths)
        fbr_band.setStyle(TableStyle([
            ("BACKGROUND",   (0, 0), (-1, -1), LGRAY),
            ("LEFTPADDING",  (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING",   (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING",(0, 0), (-1, -1), 10),
            ("VALIGN",       (0, 0), (-1, -1), "MIDDLE"),
            ("ALIGN",        (1, 0), (1, 0),   "CENTER"),
            ("LINEABOVE",    (0, 0), (-1,  0),  3, NAV),
            ("BOX",          (0, 0), (-1, -1),  0.5, MGRAY),
        ]))
        story.append(fbr_band)

        doc.build(story, onFirstPage=_page_border, onLaterPages=_page_border)

    def _save_to_s3(self, receipt_type: str) -> str:
        """Saves PDF buffer to S3 and returns URL."""
        self.buffer.seek(0)
        path       = _s3_path_for_receipt(self.sale, receipt_type)
        saved_path = default_storage.save(path, ContentFile(self.buffer.read()))
        return default_storage.url(saved_path)
