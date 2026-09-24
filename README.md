# 📄 Document AI EOB Extractor

> A sanitized, runnable Python document-AI portfolio project demonstrating PDF text extraction, structured EOB field parsing, validation, Business Central mapping, and Excel export.

[![Python CI](https://github.com/pranay-eligeti/pdf-eob-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/pranay-eligeti/pdf-eob-extractor/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![pdfplumber](https://img.shields.io/badge/pdfplumber-PDF%20parsing-red)
![Claude](https://img.shields.io/badge/Claude-optional%20LLM%20extraction-purple)

## What this repository demonstrates

I have built document-processing workflows that convert unstructured healthcare billing documents into structured data for downstream systems.

This repository is the **public, sanitized implementation of that engineering pattern**. It contains synthetic fixture data only and no PHI, employer documents, credentials, internal URLs, or proprietary source code.

### Engineering capabilities

- PDF text extraction with **pdfplumber** and **PyMuPDF** fallback
- Deterministic structured-field extraction for reproducible tests
- Optional **Anthropic Claude API** extraction provider
- Required-field validation and failure checks
- Business Central-oriented field mapping
- Excel export
- Unit tests and GitHub Actions CI

## Architecture

~~~text
PDF document
    |
    v
pdfplumber extraction
    |
    +--> PyMuPDF fallback
    |
    v
structured extraction
    |
    +--> deterministic parser
    |
    +--> optional Claude provider
    |
    v
validation
    |
    v
Business Central mapping
    |
    v
Excel export
~~~

See docs/architecture.md for design notes.

## Repository structure

~~~text
pdf-eob-extractor/
├── .github/workflows/ci.yml
├── docs/architecture.md
├── sample_data/synthetic_eob.txt
├── src/
│   ├── __init__.py
│   ├── exporter.py
│   ├── extractor.py
│   ├── mapper.py
│   ├── parser.py
│   └── validator.py
├── tests/test_document_ai.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
~~~

## Quick start

### Install

~~~bash
git clone https://github.com/pranay-eligeti/pdf-eob-extractor.git
cd pdf-eob-extractor
python -m venv .venv

# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
~~~

### Run the deterministic extraction test

~~~bash
pytest -q
~~~

### Use the PDF extractor locally

From Python, call src.extractor.extract_text(path_to_pdf) to obtain the PDF text, then pass the text to src.parser.parse_deterministic(...), validate it with src.validator, map it with src.mapper, and export with src.exporter.

### Optional Claude extraction

Set ANTHROPIC_API_KEY in a local .env file, then call src.parser.parse_with_claude(...). The provider is optional and is not used by CI.

## Example fields

The public fixture demonstrates these fields:

| Field | Example |
| --- | --- |
| claim_number | CLM-DEMO-001 |
| patient_name | Alex Example |
| service_date | 2026-08-15 |
| payer | Example Health Plan |
| billed_amount | 1250.00 |
| allowed_amount | 875.00 |
| paid_amount | 700.00 |
| patient_responsibility | 175.00 |
| adjustment_reason | CO-45 |

## Business Central mapping

The mapper produces a Cash Receipt Journal-oriented structure:

| BC field | Source |
| --- | --- |
| Document No. | Claim Number |
| Posting Date | Service Date |
| Account No. | Payer |
| Description | Patient Name + Claim Number |
| Amount | Paid Amount |
| Applies-to Doc. | Claim Number |

This public repo demonstrates the transformation only; it does not connect to a live Business Central tenant.

## Privacy and security

Never commit real EOBs, PHI, patient identifiers, credentials, employer-only documents, or production exports.

The optional Claude integration reads text supplied by the caller. Apply your organization's data-handling requirements before sending any sensitive document content to an external model provider.

## Portfolio note

The purpose of this repository is to make the document-AI engineering pattern **visible, reproducible, testable, and explainable** without publishing private healthcare systems.

## Author

**Pranay Eligeti**

[LinkedIn](https://www.linkedin.com/in/pranay-eligeti) · [GitHub](https://github.com/pranay-eligeti)
