"""
Find SRO Schedule No + Item Serial No for HS code 9819.1300 (Commission Agents)
across all non-zero Services tax rates (15%, 16%, 17%, 18.5%).

Uses the CORRECT param name discovered earlier: sroId (not sro_id).

Run like:
  FBR_SANDBOX_TOKEN="your-token-here" python find_sro_v2.py
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

DATE = "14-Jul-2026"
PROVINCE_ID = 7  # Punjab
TRANS_TYPE_ID = 18  # Services
HS_CODE = "9819.1300"

# Rate IDs for Services (Punjab) discovered earlier via SaleTypeToRate
RATE_IDS = {
    "15%": 614,
    "16%": 22,
    "17%": 92,
    "18.5%": 430,
}


def get_sro_schedules(rate_id, label):
    print(f"\n=== SroSchedule — rate={label} (rateId={rate_id}), Services, Punjab ===")
    url = "https://gw.fbr.gov.pk/pdi/v1/SroSchedule"
    params = {
        "rate_id": rate_id,
        "date": DATE,
        "origination_supplier_csv": PROVINCE_ID,
    }
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
        print("status:", resp.status_code)
        data = resp.json() if resp.status_code == 200 else None
        if data:
            for item in data:
                print("  SCHEDULE:", item)
        return data or []
    except Exception as e:
        print("ERROR:", e)
        return []


def get_sro_items(sro_id, schedule_desc):
    print(f"  -- SROItem for schedule id={sro_id} ({schedule_desc}) --")
    url = "https://gw.fbr.gov.pk/pdi/v2/SROItem"
    params = {
        "date": DATE,
        "sroId": sro_id,   # CORRECT param name
    }
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
        status = resp.status_code
        data = resp.json() if status == 200 else None
        if not data:
            print(f"     status={status} items=0")
            return
        print(f"     status={status} total_items={len(data)}")
        matches = [i for i in data if HS_CODE.replace(".", "") in str(i).replace(".", "")]
        if matches:
            for m in matches:
                print("     *** MATCH ***", m)
        else:
            print("     no direct HS match. First 3 items for inspection:")
            for i in data[:3]:
                print("      ", i)
    except Exception as e:
        print("     ERROR:", e)


if __name__ == "__main__":
    seen_schedule_ids = set()
    for label, rate_id in RATE_IDS.items():
        schedules = get_sro_schedules(rate_id, label)
        for sched in schedules:
            sro_id = sched.get("srO_ID") or sched.get("sro_id") or sched.get("id")
            desc = sched.get("srO_DESC", "")
            if sro_id and sro_id not in seen_schedule_ids:
                seen_schedule_ids.add(sro_id)
                get_sro_items(sro_id, desc)

    print(f"\n=== Checked {len(seen_schedule_ids)} unique SRO schedules total ===")
    print("If no MATCH appeared above, HS 9819.1300 is not itemized under any")
    print("SRO schedule available for Services in Punjab — meaning non-zero")
    print("percentage rates may not be usable for this HS code, and 0%/Exempt")
    print("remains the only validated path.")