"""Map extracted EOB fields to a Business Central-ready schema."""

from __future__ import annotations

from typing import Any


BC_COLUMNS = [
    "Document No.",
    "Posting Date",
    "Account No.",
    "Description",
    "Amount",
    "Applies-to Doc.",
]


def map_to_business_central(record: dict[str, Any]) -> dict[str, Any]:
    claim = record.get("claim_number", "")
    patient = record.get("patient_name", "")
    payer = record.get("payer", "")
    return {
        "Document No.": claim,
        "Posting Date": record.get("service_date", ""),
        "Account No.": payer,
        "Description": f"{patient} + {claim}".strip(" +"),
        "Amount": record.get("paid_amount"),
        "Applies-to Doc.": claim,
    }
