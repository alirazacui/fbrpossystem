"""
Find the item serial number for HS code 9819.1300 within the SRO schedules
that were confirmed valid for rateId=280 (0%), transTypeId=18 (Services), Punjab:

  387 - FIFTH SCHEDULE
  438 - ICTO
  426 - ICTO TABLE II

The first attempt at SROItem returned HTTP 500 for all three schedule ids,
which usually means a required query param is missing or named differently
than what we guessed (sro_id / date). This script tries several plausible
param-name combinations for each schedule id so we can see which shape the
endpoint actually expects.

Run like:
  FBR_SANDBOX_TOKEN="your-token-here" python find_sro_items.py
"""
import os
import json
import requests

TOKEN = os.environ.get("FBR_SANDBOX_TOKEN")
if not TOKEN:
    raise SystemExit("Set FBR_SANDBOX_TOKEN environment variable first.")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
}

DATE = "13-Jul-2026"
HS_CODE = "9819.1300"
SRO_IDS = [387, 438, 426]

# Different possible param-name shapes for the same endpoint.
# We try each shape against each candidate URL casing/path, since PRAL's
# docs are sometimes inconsistent between v1/v2 and casing.
CANDIDATE_URLS = [
    "https://gw.fbr.gov.pk/pdi/v2/SROItem",
    "https://gw.fbr.gov.pk/pdi/v1/SROItem",
    "https://gw.fbr.gov.pk/pdi/v2/SroItem",
]

PARAM_SHAPES = [
    {"date": DATE, "sro_id": None},
    {"date": DATE, "sroId": None},
    {"Date": DATE, "SRO_ID": None},
    {"date": DATE, "SRO_ID": None},
    {"rate_id": 280, "date": DATE, "sro_id": None},
]


def try_combo(url, params_template, sro_id):
    params = dict(params_template)
    for key in list(params.keys()):
        if params[key] is None:
            params[key] = sro_id
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=20)
        ok = resp.status_code == 200
        preview = ""
        if ok:
            try:
                data = resp.json()
                preview = f"items={len(data)}" if isinstance(data, list) else str(data)[:120]
            except Exception:
                preview = resp.text[:120]
        else:
            preview = resp.text[:200]
        return resp.status_code, params, preview, (resp.json() if ok else None)
    except Exception as e:
        return "ERR", params, str(e), None


def main():
    found_any_200 = False
    for sro_id in SRO_IDS:
        print(f"\n########## SRO schedule id={sro_id} ##########")
        for url in CANDIDATE_URLS:
            for shape in PARAM_SHAPES:
                status, params, preview, data = try_combo(url, shape, sro_id)
                print(f"  url={url}\n    params={params}\n    -> status={status} | {preview}")
                if status == 200:
                    found_any_200 = True
                    if data:
                        matches = [
                            i for i in data
                            if HS_CODE.replace(".", "") in str(i).replace(".", "")
                        ]
                        if matches:
                            print("    *** MATCH for our HS code ***")
                            for m in matches:
                                print("     ", m)
                        elif isinstance(data, list) and data:
                            print("    (200 OK, no direct HS match — first item for inspection):")
                            print("     ", data[0])

    if not found_any_200:
        print("\nNo combination returned 200. Next step: pull the exact endpoint name/params")
        print("from the PRAL 'TechnicalDocumentationforDIAPIV1.12.pdf' Reference APIs section")
        print("(search for 'SRO Item' or 'Item' under Reference APIs) and paste the exact")
        print("path + param names here so the script can be corrected precisely.")


if __name__ == "__main__":
    main()