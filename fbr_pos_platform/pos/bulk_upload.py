"""
========================================================
pos/bulk_upload.py

Bulk Product Upload — Parse & Validate View

Flow:
  1. POST /api/products/parse-bulk/
     → Accepts .xlsx or .csv file
     → Parses rows using openpyxl / csv
     → Validates required fields and HS/PCT code format
     → Returns structured JSON (no DB writes)

  2. Frontend loops through returned rows one-by-one
     → POST /api/products/ for each row (existing endpoint)
     → Live progress updates in UI per row

Supported column names (case-insensitive, aliases supported):
  Name            → name
  Cost Price      → cost_price
  Retail Price    → selling_price
  Selling Price   → selling_price
  Sale Price      → selling_price
  Tax Rate        → tax_rate_percent
  Tax Rate %      → tax_rate_percent
  HS Code         → hs_code
  PCT Code        → hs_code  (we store in hs_code; model auto-syncs pct_code)
  HS/PCT Code     → hs_code
  Barcode         → barcode
  SKU             → sku
  Initial Stock   → current_stock
  Stock           → current_stock
  Category        → category_name  (resolved to ID at save time)
  Unit            → unit_of_measure
  Unit of Measure → unit_of_measure
  Sale Type       → fbr_sale_type
  FBR Sale Type   → fbr_sale_type
========================================================
"""

import csv
import io
import re
import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from common.permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)

# ── Valid values for server-side validation ──────────────────────────────────

VALID_TAX_RATES = {"0%", "5%", "8%", "15%", "16%", "17%", "18%", "25%", "exempt"}

VALID_FBR_SALE_TYPES = {
    "Goods at standard rate (default)",
    "3rd Schedule Goods",
    "Goods at Reduced Rate",
    "Goods at zero-rate",
    "Exempt Goods",
    "Electric Vehicle",
    "Mobile Phones",
    "CNG Sales",
    "Cement /Concrete Block",
    "Cotton Ginners",
    "Electricity Supply to Retailers",
    "Gas to CNG stations",
    "Goods as per SRO.297(|)/2023",
    "Goods (FED in ST Mode)",
    "Non-Adjustable Supplies",
    "Petroleum Products",
    "Potassium Chlorate",
    "Processing/ Conversion of Goods",
    "Services",
    "Services (FED in ST Mode)",
    "Ship breaking",
    "Steel Melting and re-rolling",
    "Telecommunication services",
    "Toll Manufacturing",
}

# User-friendly Sale Type aliases → canonical FBR value
# Covers common labels people type in Excel sheets
FBR_SALE_TYPE_ALIASES = {
    "standard rate (general goods)": "Goods at standard rate (default)",
    "standard rate": "Goods at standard rate (default)",
    "standard": "Goods at standard rate (default)",
    "goods at standard rate": "Goods at standard rate (default)",
    "general goods": "Goods at standard rate (default)",
    "default": "Goods at standard rate (default)",
    "reduced rate": "Goods at Reduced Rate",
    "goods at reduced rate": "Goods at Reduced Rate",
    "reduced": "Goods at Reduced Rate",
    "8th schedule": "Goods at Reduced Rate",
    "zero rated": "Goods at zero-rate",
    "zero-rated": "Goods at zero-rate",
    "zero rate": "Goods at zero-rate",
    "0%": "Goods at zero-rate",
    "exempt": "Exempt Goods",
    "exempted": "Exempt Goods",
    "3rd schedule": "3rd Schedule Goods",
    "third schedule": "3rd Schedule Goods",
    "services": "Services",
    "service": "Services",
    "ev": "Electric Vehicle",
    "electric vehicle": "Electric Vehicle",
    "mobile": "Mobile Phones",
    "mobile phones": "Mobile Phones",
    "cng": "CNG Sales",
    "cement": "Cement /Concrete Block",
    "petroleum": "Petroleum Products",
}

# UOM aliases → canonical FBR UOM string
UOM_ALIASES = {
    "numbers": "Numbers, pieces, units",
    "number": "Numbers, pieces, units",
    "pieces": "Numbers, pieces, units",
    "piece": "Piece",
    "pcs": "Numbers, pieces, units",
    "units": "Numbers, pieces, units",
    "unit": "Numbers, pieces, units",
    "nos": "Numbers, pieces, units",
    "no.": "Numbers, pieces, units",
    "each": "Numbers, pieces, units",
    "ea": "Numbers, pieces, units",
    "kg": "KG",
    "kilogram": "KG",
    "kilograms": "KG",
    "gram": "Gram",
    "grams": "Gram",
    "gm": "Gram",
    "g": "Gram",
    "litre": "Litre",
    "liter": "Litre",
    "litres": "Litre",
    "liters": "Litre",
    "l": "Litre",
    "ml": "Litre",
    "metre": "Metre",
    "meter": "Metre",
    "meters": "Metre",
    "metres": "Metre",
    "m": "Metre",
    "box": "Box",
    "boxes": "Box",
    "carton": "Carton",
    "cartons": "Carton",
    "bag": "Bag",
    "bags": "Bag",
    "bottle": "Bottle",
    "bottles": "Bottle",
    "dozen": "Dozen",
    "doz": "Dozen",
    "pair": "Pair",
    "pairs": "Pair",
    "set": "Set",
    "sets": "Set",
    "pack": "Pack",
    "packs": "Pack",
    "packet": "Pack",
    "packets": "Pack",
    "roll": "Roll",
    "rolls": "Roll",
    "sheet": "Sheet",
    "sheets": "Sheet",
    "ton": "Ton",
    "tons": "Ton",
    "metric ton": "Metric Ton",
    "mt": "Metric Ton",
    "barrel": "Barrels",
    "barrels": "Barrels",
    "drum": "Drum",
    "drums": "Drum",
    "yard": "Yard",
    "yards": "Yard",
    "foot": "Foot",
    "feet": "Foot",
    "ft": "Foot",
    "inch": "Inch",
    "inches": "Inch",
    "in": "Inch",
    "service": "Service",
    "services": "Service",
}

VALID_UOM = {
    "Numbers, pieces, units", "1000 kWh", "40 KG", "Bag", "Barrels",
    "Bill of Lading", "Bottle", "Box", "Bundle", "Carat", "Carton", "Case",
    "Cubic Metre", "Dozen", "Drum", "Foot", "Gallon", "Gram", "Inch", "KG",
    "KWH", "Litre", "Mega Watt (MW)", "Metre", "Metric Ton",
    "Million BTU (MMBTU)", "Pack", "Pair", "Pallet", "Piece", "Roll",
    "Set", "Sheet", "Service", "Square Foot", "Square Metre", "Ton", "Tube", "Yard",
}

# Column header aliases → canonical field name
COLUMN_MAP = {
    # ── Identity ──────────────────────────────────────────────────────────────
    "name":                  "name",
    "product name":          "name",
    "item name":             "name",
    # ── Pricing ───────────────────────────────────────────────────────────────
    "cost price":            "cost_price",
    "cost":                  "cost_price",
    "purchase price":        "cost_price",
    "selling price":         "selling_price",
    "sale price":            "selling_price",
    "price":                 "selling_price",
    "retail price":          "fbr_fixed_retail_price",  # fixed FBR retail / 3rd schedule
    "fixed retail price":    "fbr_fixed_retail_price",
    "fbr retail price":      "fbr_fixed_retail_price",
    "notified value":        "fbr_fixed_retail_price",
    # ── Tax ───────────────────────────────────────────────────────────────────
    "tax rate":              "tax_rate_percent",
    "tax rate %":            "tax_rate_percent",
    "tax %":                 "tax_rate_percent",
    "tax":                   "tax_rate_percent",
    # ── FBR classification ────────────────────────────────────────────────────
    "hs code":               "hs_code",
    "hs/pct code":           "hs_code",
    "pct code":              "hs_code",
    "hs code / pct code":    "hs_code",
    "sale type":             "fbr_sale_type",
    "fbr sale type":         "fbr_sale_type",
    "type":                  "fbr_sale_type",
    # ── SRO ───────────────────────────────────────────────────────────────────
    "sro schedule":          "fbr_sro_schedule_no",
    "sro schedule no":       "fbr_sro_schedule_no",
    "sro":                   "fbr_sro_schedule_no",
    "sro item serial":       "fbr_sro_item_serial_no",
    "sro serial":            "fbr_sro_item_serial_no",
    "sro serial no":         "fbr_sro_item_serial_no",
    "sro item serial no":    "fbr_sro_item_serial_no",
    # ── Unit of Measure ───────────────────────────────────────────────────────
    "unit":                  "unit_of_measure",
    "unit of measure":       "unit_of_measure",
    "uom":                   "unit_of_measure",
    # ── Inventory ─────────────────────────────────────────────────────────────
    "barcode":               "barcode",
    "sku":                   "sku",
    "initial stock":         "current_stock",
    "stock":                 "current_stock",
    "current stock":         "current_stock",
    "opening stock":         "current_stock",
    "reorder level":         "low_stock_threshold",
    "low stock threshold":   "low_stock_threshold",
    "reorder":               "low_stock_threshold",
    "track inventory":       "track_inventory",
    "track stock":           "track_inventory",
    # ── Category & description ────────────────────────────────────────────────
    "category":              "category_name",
    "category name":         "category_name",
    "description":           "description",
}


def normalize_tax_rate(raw: str) -> str:
    """
    Normalize tax rate input.
    '18'  → '18%'
    '18%' → '18%'
    'exempt' → 'Exempt'
    Returns normalized string or empty string if unrecognized.
    """
    v = raw.strip()
    if v.lower() == "exempt":
        return "Exempt"
    # Strip % and try to parse as number
    numeric = v.replace("%", "").strip()
    try:
        num = float(numeric)
        # Round to 0 decimal if whole number
        if num == int(num):
            return f"{int(num)}%"
        return f"{num}%"
    except ValueError:
        return v  # Return as-is — validation will catch it


def normalize_hs_code(raw: str) -> str:
    """
    Normalizes the HS Code / PCT Code.
    We just strip whitespace and keep what the user typed.
    The Product model's save() will auto-generate pct_code by removing any dots.
    """
    v = raw.strip()
    if not v:
        return v
    return v


def validate_row(row: dict, row_number: int) -> list:
    """
    Validate a single parsed row.
    Returns a list of validation error strings (empty list = valid).
    """
    errors = []
    
    # ── Required fields ──────────────────────────────────────────────────────
    name = (row.get("name") or "").strip()
    if not name:
        errors.append("Name is required.")
    
    selling_price = row.get("selling_price")
    if selling_price is None or selling_price == "":
        errors.append("Selling Price is required.")
    else:
        try:
            price_val = float(selling_price)
            if price_val < 0:
                errors.append("Selling Price must be a positive number.")
        except (ValueError, TypeError):
            errors.append(f"Selling Price '{selling_price}' is not a valid number.")
    
    # ── Tax Rate ─────────────────────────────────────────────────────────────
    tax_rate = (row.get("tax_rate_percent") or "").strip()
    if tax_rate:
        normalized = normalize_tax_rate(tax_rate)
        if normalized.lower() not in VALID_TAX_RATES:
            errors.append(
                f"Tax Rate '{tax_rate}' is not valid. "
                f"Use: 18%, 17%, 16%, 15%, 8%, 5%, 0%, or Exempt."
            )
        else:
            row["tax_rate_percent"] = normalized  # Update in-place
    else:
        row["tax_rate_percent"] = "18%"  # Default
    
    # ── HS Code ──────────────────────────────────────────────────────────────
    hs_code = (row.get("hs_code") or "").strip()
    if hs_code:
        normalized_hs = normalize_hs_code(hs_code)
        row["hs_code"] = normalized_hs
        # Validate format: should have digits and optionally a dot
        clean = re.sub(r"[.\s]", "", normalized_hs)
        if not clean.isdigit():
            errors.append(
                f"HS Code '{hs_code}' contains invalid characters. "
                "Must be numeric digits only (e.g. 2106.9090 or 21069090)."
            )
        elif len(clean) < 4:
            errors.append(
                f"HS Code '{hs_code}' is too short. "
                "Minimum 4 digits required."
            )
    
    # ── Cost Price ───────────────────────────────────────────────────────────
    cost_price = row.get("cost_price")
    if cost_price is not None and cost_price != "":
        try:
            cp = float(cost_price)
            if cp < 0:
                errors.append("Cost Price must be a positive number.")
        except (ValueError, TypeError):
            errors.append(f"Cost Price '{cost_price}' is not a valid number.")
    
    # ── Stock ────────────────────────────────────────────────────────────────
    stock = row.get("current_stock")
    if stock is not None and stock != "":
        try:
            float(stock)
        except (ValueError, TypeError):
            errors.append(f"Stock '{stock}' is not a valid number.")
    
    # ── FBR Sale Type — normalize via alias map, silently correct unknown values ──
    fbr_sale_type = (row.get("fbr_sale_type") or "").strip()
    if fbr_sale_type:
        if fbr_sale_type not in VALID_FBR_SALE_TYPES:
            # Try alias lookup (case-insensitive)
            alias_key = fbr_sale_type.lower()
            canonical = FBR_SALE_TYPE_ALIASES.get(alias_key)
            if canonical:
                row["fbr_sale_type"] = canonical  # silently corrected ✅
            else:
                # Unknown but not critical — default silently
                row["fbr_sale_type"] = "Goods at standard rate (default)"
    else:
        row["fbr_sale_type"] = "Goods at standard rate (default)"

    # ── Unit of Measure — normalize via alias map ─────────────────────────────
    uom = (row.get("unit_of_measure") or "").strip()
    if uom and uom not in VALID_UOM:
        alias_key = uom.lower()
        canonical_uom = UOM_ALIASES.get(alias_key)
        if canonical_uom:
            row["unit_of_measure"] = canonical_uom  # silently corrected ✅
        # If still unknown, keep original — Django will accept or reject
    
    return errors


def parse_headers(raw_headers: list) -> dict:
    """
    Map raw column headers (from Excel/CSV) to canonical field names.
    Returns a dict: {column_index: canonical_field_name}
    Unrecognized columns are skipped.
    """
    mapping = {}
    for idx, header in enumerate(raw_headers):
        key = header.strip().lower()
        if key in COLUMN_MAP:
            mapping[idx] = COLUMN_MAP[key]
    return mapping


def parse_excel(file_bytes: bytes) -> list:
    """Parse .xlsx file bytes, return list of row dicts."""
    import openpyxl
    wb = openpyxl.load_workbook(
        filename=io.BytesIO(file_bytes),
        read_only=True,
        data_only=True,
    )
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []
    
    header_row = [str(cell).strip() if cell is not None else "" for cell in rows[0]]
    col_map = parse_headers(header_row)
    
    result = []
    for row_data in rows[1:]:
        # Skip completely empty rows
        if all(cell is None or str(cell).strip() == "" for cell in row_data):
            continue
        row = {}
        for idx, canonical in col_map.items():
            if idx < len(row_data):
                val = row_data[idx]
                row[canonical] = str(val).strip() if val is not None else ""
        result.append(row)
    
    return result


def parse_csv(file_bytes: bytes) -> list:
    """Parse .csv file bytes, return list of row dicts."""
    text = file_bytes.decode("utf-8-sig")  # handle BOM
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows:
        return []
    
    col_map = parse_headers(rows[0])
    result = []
    for row_data in rows[1:]:
        if all(cell.strip() == "" for cell in row_data):
            continue
        row = {}
        for idx, canonical in col_map.items():
            if idx < len(row_data):
                row[canonical] = row_data[idx].strip()
        result.append(row)
    
    return result


class BulkProductParseView(APIView):
    """
    POST /api/products/parse-bulk/

    Accepts a multipart file upload (field name: 'file').
    Supports .xlsx and .csv formats.

    Returns:
    {
        "total_rows": 50,
        "valid_rows": 48,
        "invalid_rows": 2,
        "columns_detected": ["name", "selling_price", ...],
        "rows": [
            {
                "row_number": 2,
                "status": "valid",
                "errors": [],
                "data": {
                    "name": "Pepsi 1.5L",
                    "selling_price": "150",
                    "cost_price": "100",
                    "tax_rate_percent": "18%",
                    "hs_code": "2202.1000",
                    "barcode": "",
                    "sku": "",
                    "current_stock": "100",
                    "category_name": "Beverages",
                    "unit_of_measure": "Numbers, pieces, units",
                    "fbr_sale_type": "Goods at standard rate (default)"
                }
            },
            ...
        ]
    }
    """
    permission_classes = [IsOwnerOrAdmin]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"detail": "No file uploaded. Please upload a .xlsx or .csv file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        filename = file.name.lower()
        if not (filename.endswith(".xlsx") or filename.endswith(".csv")):
            return Response(
                {"detail": "Unsupported file format. Please upload a .xlsx or .csv file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # File size guard (max 5 MB)
        if file.size > 5 * 1024 * 1024:
            return Response(
                {"detail": "File is too large. Maximum allowed size is 5 MB."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        file_bytes = file.read()
        
        try:
            if filename.endswith(".xlsx"):
                raw_rows = parse_excel(file_bytes)
            else:
                raw_rows = parse_csv(file_bytes)
        except Exception as e:
            logger.error(f"[BulkUpload] Failed to parse file: {e}")
            return Response(
                {"detail": f"Failed to read file: {str(e)}. Make sure it is a valid Excel or CSV file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if not raw_rows:
            return Response(
                {"detail": "The file is empty or has no data rows. Please check the file and try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if len(raw_rows) > 500:
            return Response(
                {"detail": f"File contains {len(raw_rows)} rows. Maximum allowed is 500 rows per upload. Please split the file."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # ── Set defaults for optional fields ─────────────────────────────
        for row in raw_rows:
            row.setdefault("tax_rate_percent",        "18%")
            row.setdefault("fbr_sale_type",           "Goods at standard rate (default)")
            row.setdefault("unit_of_measure",         "Numbers, pieces, units")
            row.setdefault("current_stock",           "0")
            row.setdefault("cost_price",              "")
            row.setdefault("barcode",                 "")
            row.setdefault("sku",                     "")
            row.setdefault("hs_code",                 "")
            row.setdefault("category_name",           "")
            row.setdefault("description",             "")
            row.setdefault("fbr_fixed_retail_price",  "")
            row.setdefault("fbr_sro_schedule_no",     "")
            row.setdefault("fbr_sro_item_serial_no",  "")
            row.setdefault("low_stock_threshold",     "")
            row.setdefault("track_inventory",         "")
        
        # ── Validate each row ─────────────────────────────────────────────
        parsed_rows = []
        valid_count = 0
        invalid_count = 0
        
        for i, row in enumerate(raw_rows, start=2):  # Row 1 = headers, so data starts at 2
            errors = validate_row(row, i)
            row_status = "valid" if not errors else "invalid"
            if row_status == "valid":
                valid_count += 1
            else:
                invalid_count += 1
            
            parsed_rows.append({
                "row_number": i,
                "status": row_status,
                "errors": errors,
                "data": row,
            })
        
        # Detect which canonical fields were found
        columns_detected = sorted(set(
            field for row_entry in parsed_rows
            for field in row_entry["data"].keys()
        ))
        
        return Response({
            "total_rows":       len(raw_rows),
            "valid_rows":       valid_count,
            "invalid_rows":     invalid_count,
            "columns_detected": columns_detected,
            "rows":             parsed_rows,
        }, status=status.HTTP_200_OK)
