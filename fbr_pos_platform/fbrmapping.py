"""
FBR Sandbox verification script — Commission Agent Service (HS Code 98191300)

Purpose:
  1. Fetch valid UOM(s) for HS code 98191300 (real values, not guessed)
  2. Fetch full transaction type list, so we can find the right transTypeId for Services
  3. Fetch valid rate(s) for that transaction type + province, to confirm 0% is correct
  4. Check the generic UOM list for a "Service" / countable-unit option

IMPORTANT: Put your token in an environment variable, never hardcode it in a file
you might commit to git or share.

Run like:
  FBR_SANDBOX_TOKEN="your-token-here" python fbrmapping.py
"""

import os
import requests

TOKEN = os.environ.get("FBR_SANDBOX_TOKEN")
if not TOKEN:
    raise SystemExit("Set FBR_SANDBOX_TOKEN environment variable first.")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

HS_CODE = "98191300"
DATE = "13-Jul-2026"


def find_exact_hs_code():
    """Search the official item catalogue for how 98191300 is actually stored."""
    print("\n=== 0. itemdesccode — searching catalogue for HS code", HS_CODE, "===")
    url = "https://gw.fbr.gov.pk/pdi/v1/itemdesccode"
    found = []
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        print("status:", resp.status_code, " total_items:", len(resp.json()) if resp.status_code == 200 else 0)
        if resp.status_code == 200:
            data = resp.json()
            digits_only = HS_CODE
            for item in data:
                code = item.get("hS_CODE", "")
                desc = item.get("description", "")
                code_digits = code.replace(".", "").replace(" ", "")
                if code_digits == digits_only or "commission" in desc.lower():
                    found.append(item)
            for f in found:
                print("  MATCH:", f)
            if not found:
                print("  No match found for HS code or 'commission' in descriptions.")
    except Exception as e:
        print("ERROR:", e)
    return [f["hS_CODE"] for f in found] if found else [HS_CODE]


def check_hs_uom(exact_codes):
    print("\n=== 1. HS_UOM — valid UOM(s) for HS code", HS_CODE, "===")
    url = "https://gw.fbr.gov.pk/pdi/v2/HS_UOM"
    any_hit = False
    for code in exact_codes:
        for annexure_id in range(1, 11):
            params = {"hs_code": code, "annexure_id": annexure_id}
            try:
                resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
                result = resp.json() if resp.status_code == 200 else None
                if result:
                    any_hit = True
                    print(f"hs_code={code} annexure_id={annexure_id} -> status={resp.status_code} data={result}")
            except Exception as e:
                print(f"hs_code={code} annexure_id={annexure_id} -> ERROR: {e}")
    if not any_hit:
        print("  No UOM mapping found for this HS code in annexure_id 1-10 (expected for Chapter 98 service codes).")


def check_generic_uom_list():
    print("\n=== 1b. uom — full generic UOM list, searching for 'service'/generic countable options ===")
    url = "https://gw.fbr.gov.pk/pdi/v1/uom"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        print("status:", resp.status_code)
        if resp.status_code == 200:
            data = resp.json()
            print(f"  total UOMs: {len(data)}")
            for item in data:
                desc = item.get("description", "")
                if any(k in desc.lower() for k in ["service", "number", "piece", "unit", "each", "nos"]):
                    print("  CANDIDATE:", item)
    except Exception as e:
        print("ERROR:", e)

    print("\n=== 2. transtypecode — full transaction type list ===")
    url = "https://gw.fbr.gov.pk/pdi/v1/transtypecode"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        print("status:", resp.status_code)
        if resp.status_code == 200:
            data = resp.json()
            matched_any = False
            for item in data:
                desc = item.get("transactioN_DESC", "")
                if any(k in desc.lower() for k in ["service", "commission", "agent"]):
                    print("  MATCH:", item)
                    matched_any = True
            print(f"\n  (total {len(data)} transaction types returned)")
            if not matched_any:
                print("  No obvious match — full list:")
                for item in data:
                    print("   ", item)
    except Exception as e:
        print("ERROR:", e)


def check_provinces():
    print("\n=== 3. provinces — to get your originationSupplier province code ===")
    url = "https://gw.fbr.gov.pk/pdi/v1/provinces"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        print("status:", resp.status_code)
        if resp.status_code == 200:
            print(resp.json())
    except Exception as e:
        print("ERROR:", e)


def check_rate(trans_type_id, province_id):
    print(f"\n=== 4. SaleTypeToRate — for transTypeId={trans_type_id}, province={province_id} ===")
    url = "https://gw.fbr.gov.pk/pdi/v2/SaleTypeToRate"
    params = {"date": DATE, "transTypeId": trans_type_id, "originationSupplier": province_id}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
        print("status:", resp.status_code)
        if resp.status_code == 200:
            print(resp.json())
    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    exact_codes = find_exact_hs_code()
    check_hs_uom(exact_codes)
    check_generic_uom_list()
    check_provinces()
    # transTypeId=18 confirmed as "Services".
    # Checking BOTH provinces — client is actually registered in Punjab (7),
    # earlier check was mistakenly run against Sindh (8) only.
    check_rate(trans_type_id=18, province_id=7)   # Punjab — client's actual province
    check_rate(trans_type_id=18, province_id=8)   # Sindh — for comparison only