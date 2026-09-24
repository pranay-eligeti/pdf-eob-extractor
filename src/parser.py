"""Structured EOB field extraction.

The deterministic parser is used by the public demo. Claude can be added as
an optional extraction provider for less-structured production documents.
"""

from __future__ import annotations

import json
import re
import os
from typing import Any

from anthropic import Anthropic


FIELD_PATTERNS = {
    "claim_number": r"Claim Number:\s*(.+)",
    "patient_name": r"Patient Name:\s*(.+)",
    "service_date": r"Service Date:\s*(.+)",
    "payer": r"Payer:\s*(.+)",
    "billed_amount": r"Billed Amount:\s*\$?([0-9,.]+)",
    "allowed_amount": r"Allowed Amount:\s*\$?([0-9,.]+)",
    "paid_amount": r"Paid Amount:\s*\$?([0-9,.]+)",
    "patient_responsibility": r"Patient Responsibility:\s*\$?([0-9,.]+)",
    "adjustment_reason": r"Adjustment Reason:\s*(.+)",
}


def _clean_amount(value: str) -> float:
    return float(value.replace(",", ""))


def parse_deterministic(text: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = re.search(pattern, text, re.I)
        if not match:
            continue
        value = match.group(1).strip()
        result[field] = _clean_amount(value) if field.endswith("amount") or field == "patient_responsibility" else value
    return result


def parse_with_claude(text: str, model: str = "claude-3-5-sonnet-latest") -> dict[str, Any]:
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = (
        "Extract the following EOB fields as strict JSON. Return only JSON. "
        "Use null for missing values. Never invent values. Fields: "
        "claim_number, patient_name, service_date, payer, billed_amount, "
        "allowed_amount, paid_amount, patient_responsibility, adjustment_reason.\n\n"
        f"EOB text:\n{text}"
    )
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    block = message.content[0]
    raw = getattr(block, "text", str(block)).strip()
    return json.loads(raw)
