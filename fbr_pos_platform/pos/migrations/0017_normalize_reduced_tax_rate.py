from django.db import migrations


def forwards(apps, schema_editor):
    Product = apps.get_model("pos", "Product")
    SaleLine = apps.get_model("pos", "SaleLine")
    SaleReturnLine = apps.get_model("pos", "SaleReturnLine")
    DebitNoteLine = apps.get_model("pos", "DebitNoteLine")

    for model in (Product, SaleLine, SaleReturnLine, DebitNoteLine):
        model.objects.filter(tax_rate_percent="8%").update(tax_rate_percent="5%")


def backwards(apps, schema_editor):
    Product = apps.get_model("pos", "Product")
    SaleLine = apps.get_model("pos", "SaleLine")
    SaleReturnLine = apps.get_model("pos", "SaleReturnLine")
    DebitNoteLine = apps.get_model("pos", "DebitNoteLine")

    for model in (Product, SaleLine, SaleReturnLine, DebitNoteLine):
        model.objects.filter(tax_rate_percent="5%").update(tax_rate_percent="8%")


class Migration(migrations.Migration):

    dependencies = [
        ("pos", "0016_seed_hs_codes"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]