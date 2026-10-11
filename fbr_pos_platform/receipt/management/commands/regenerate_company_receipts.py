from django.core.management.base import BaseCommand, CommandError

from pos.models import Sale
from receipt.generators import A4InvoiceGenerator, ThermalReceiptGenerator


class Command(BaseCommand):
    help = (
        "Regenerate stored thermal and/or A4 PDFs for a company, so old cached"
        " invoices reflect the latest client_type label (FBR vs PRA)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--company-id", type=int, help="Company ID to regenerate.")
        parser.add_argument("--company-ntn", type=str, help="Company NTN to regenerate.")
        parser.add_argument(
            "--limit",
            type=int,
            default=0,
            help="Optional max number of sales to regenerate. 0 means all.",
        )
        parser.add_argument(
            "--skip-thermal",
            action="store_true",
            help="Do not regenerate the thermal receipt PDF.",
        )
        parser.add_argument(
            "--skip-a4",
            action="store_true",
            help="Do not regenerate the A4 invoice PDF.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview the sales that would be regenerated without creating PDFs.",
        )

    def handle(self, *args, **options):
        company_id = options.get("company_id")
        company_ntn = options.get("company_ntn")

        if not company_id and not company_ntn:
            raise CommandError("Provide either --company-id or --company-ntn.")

        qs = Sale.objects.select_related("company", "customer", "cashier").order_by("completed_at", "id")
        if company_id:
            qs = qs.filter(company_id=company_id)
        if company_ntn:
            qs = qs.filter(company__ntn=company_ntn)

        total = qs.count()
        if total == 0:
            raise CommandError("No sales were found for the requested company.")

        self.stdout.write(
            self.style.WARNING(
                f"Found {total} sales for this company. "
                f"Regenerating {'thermal + A4' if not (options['skip_thermal'] and options['skip_a4']) else 'nothing'}"
            )
        )

        processed = 0
        for sale in qs:
            if options["limit"] and processed >= options["limit"]:
                break

            if options["dry_run"]:
                self.stdout.write(f"DRY RUN: {sale.sale_number} ({sale.id})")
                processed += 1
                continue

            if not options["skip_thermal"]:
                ThermalReceiptGenerator(sale).generate(force_regenerate=True)
                self.stdout.write(f"Regenerated thermal: {sale.sale_number}")

            if not options["skip_a4"]:
                A4InvoiceGenerator(sale).generate(force_regenerate=True)
                self.stdout.write(f"Regenerated A4: {sale.sale_number}")

            processed += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Completed regeneration for {processed} sales."
            )
        )
