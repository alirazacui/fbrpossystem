import csv
import json
import os
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from pos.models import HSCode

REPO_ROOT = Path(__file__).resolve().parent.parent
PCT_CSV = REPO_ROOT / "hs_codes_pct.csv"
SERVICES_CSV = REPO_ROOT / "hs_codes_services.csv"
FRONTEND_JSON = REPO_ROOT / "fbr_pos_frontend" / "src" / "assets" / "hs_codes.json"


def _normalize_code(value):
    if value is None:
        return ""
    return str(value).strip()


def _normalize_description(value):
    if value is None:
        return ""
    return str(value).strip()


def load_pct_csv(path):
    items = []
    if not path.exists():
        return items

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            code = _normalize_code(row.get("PCT Code"))
            description = _normalize_description(row.get("Description"))
            if code and description:
                items.append({"code": code, "description": description})
    return items


def load_services_csv(path):
    items = []
    if not path.exists():
        return items

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            code = _normalize_code(row.get("HS Code"))
            description = _normalize_description(row.get("Description"))
            if code and description:
                items.append({"code": code, "description": description})
    return items


def load_frontend_json(path):
    items = []
    if not path.exists():
        return items

    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    for row in data:
        code = _normalize_code(row.get("code"))
        description = _normalize_description(row.get("description"))
        if code and description:
            items.append({"code": code, "description": description})
    return items


def load_all_items():
    items = []
    items.extend(load_pct_csv(PCT_CSV))
    items.extend(load_services_csv(SERVICES_CSV))
    items.extend(load_frontend_json(FRONTEND_JSON))

    deduped = {}
    for item in items:
        deduped[item["code"]] = item["description"]

    return [
        HSCode(code=code, description=description)
        for code, description in sorted(deduped.items(), key=lambda entry: entry[0])
    ]


if __name__ == "__main__":
    objects = load_all_items()
    print(f"Prepared {len(objects)} unique HS codes from CSV/JSON sources.")

    HSCode.objects.all().delete()
    HSCode.objects.bulk_create(objects, batch_size=1000)

    print("Done populating HS codes.")
