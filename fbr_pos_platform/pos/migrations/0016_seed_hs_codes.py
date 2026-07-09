"""
Seed the HS code catalog from the repo data files.

This migration runs once during `python manage.py migrate` and is safe to
re-run because it uses update_or_create on the HS code unique key.
"""

from csv import DictReader
from json import load as json_load
from pathlib import Path

from django.db import migrations


REPO_ROOT = Path(__file__).resolve().parents[3]
PCT_CSV = REPO_ROOT / "hs_codes_pct.csv"
SERVICES_CSV = REPO_ROOT / "hs_codes_services.csv"
FRONTEND_JSON = REPO_ROOT / "fbr_pos_frontend" / "src" / "assets" / "hs_codes.json"


def _normalize(value):
    if value is None:
        return ""
    return str(value).strip()


def load_pct_codes():
    items = []
    if not PCT_CSV.exists():
        return items

    with PCT_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = DictReader(handle)
        for row in reader:
            code = _normalize(row.get("PCT Code"))
            description = _normalize(row.get("Description"))
            if code and description:
                items.append((code, description))
    return items


def load_services_codes():
    items = []
    if not SERVICES_CSV.exists():
        return items

    with SERVICES_CSV.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = DictReader(handle)
        for row in reader:
            code = _normalize(row.get("HS Code"))
            description = _normalize(row.get("Description"))
            if code and description:
                items.append((code, description))
    return items


def load_frontend_codes():
    items = []
    if not FRONTEND_JSON.exists():
        return items

    with FRONTEND_JSON.open("r", encoding="utf-8") as handle:
        data = json_load(handle)

    for row in data:
        code = _normalize(row.get("code"))
        description = _normalize(row.get("description"))
        if code and description:
            items.append((code, description))
    return items


def load_all_codes():
    combined = {}
    for code, description in load_pct_codes() + load_services_codes() + load_frontend_codes():
        combined[code] = description
    return sorted(combined.items(), key=lambda item: item[0])


def seed_hs_codes(apps, schema_editor):
    HSCode = apps.get_model("pos", "HSCode")
    created_count = 0
    for code, description in load_all_codes():
        _, created = HSCode.objects.update_or_create(
            code=code,
            defaults={"description": description},
        )
        if created:
            created_count += 1

    print(f"\n  ✓ Seeded HS codes: {created_count} created, {HSCode.objects.count()} total present")


def unseed_hs_codes(apps, schema_editor):
    HSCode = apps.get_model("pos", "HSCode")
    codes = [code for code, _ in load_all_codes()]
    deleted, _ = HSCode.objects.filter(code__in=codes).delete()
    print(f"\n  ✓ Removed {deleted} seeded HS codes")


class Migration(migrations.Migration):
    dependencies = [
        ("pos", "0015_warehousestock"),
    ]

    operations = [
        migrations.RunPython(seed_hs_codes, reverse_code=unseed_hs_codes),
    ]
