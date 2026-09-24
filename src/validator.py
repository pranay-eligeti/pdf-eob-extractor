"""Validation for extracted and mapped document fields."""

from __future__ import annotations

from typing import Any

REQUIRED_EXTRACTION_FIELDS = [
    "claim_number",
    "patient_name",
    "service_date",
    "payer",
    "paid_amount",
]


def missing_required_fields(record: dict[str, Any]) -> list[str]:
    return [field for field in REQUIRED_EXTRACTION_FIELDS if not record.get(field)]


def validate_business_central(record: dict[str, Any]) -> list[str]:
    required = [
        "Document No.",
        "Posting Date",
        "Account No.",
        "Amount",
    ]
    return [field for field in required if not record.get(field)]
