from pos.models import FBRSubmissionStatus


def should_keep_existing_submission_result(sale) -> bool:
    """
    Prevent a later failed submission from overwriting a prior successful one.

    This is important for companies that use both POS and DI integrations.
    If either path returns a valid FBR invoice number, the sale should remain
    in a successful state even if the other path fails later.
    """
    if not sale:
        return False

    if getattr(sale, "fbr_submission_status", None) == FBRSubmissionStatus.SUCCESS:
        return True

    return bool(getattr(sale, "fbr_invoice_number", ""))
