# 📄 PDF EOB Extractor & Business Central Integration

> Automates extraction of structured billing data from Explanation of Benefits (EOB) PDFs using Python and Anthropic Claude API, then maps and posts it directly to Microsoft Dynamics 365 Business Central Cash Receipt Journals — eliminating all manual data entry.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Anthropic](https://img.shields.io/badge/Anthropic-Claude%20API-blueviolet)
![pdfplumber](https://img.shields.io/badge/pdfplumber-PDF%20Parsing-red)
![MS Dynamics 365](https://img.shields.io/badge/MS%20Dynamics%20365-Business%20Central-orange?logo=microsoft)

---

## What It Does

Reads EOB PDF files from insurance providers, intelligently extracts payment fields (claim numbers, patient names, amounts, dates, payer info) using Claude API, and outputs data structured for direct import into Microsoft Dynamics 365 Business Central's Cash Receipt Journal — via the Edit-in-Excel upload path.

---

## The Problem It Solves

EOB PDFs from different insurance providers are inconsistently formatted — no two look alike. Manual data entry into Business Central is slow, error-prone, and time-consuming for billing teams. This tool:

- Handles any EOB format automatically
- Extracts all relevant billing fields accurately
- Produces BC-ready output with no manual reformatting

---

## How It Works

```
EOB PDF (any insurance provider format)
        │
        ▼
pdfplumber / PyMuPDF
  → Extracts raw text layer from PDF
  → Handles multi-page documents
  → Identifies table structures
        │
        ▼
Anthropic Claude API
  Prompt: "Extract structured billing data from this EOB text"
  Output: {
    claim_number: "CLM-2024-001234",
    patient_name: "John Doe",
    service_date: "2024-11-15",
    payer: "Blue Cross Blue Shield",
    billed_amount: 1250.00,
    allowed_amount: 875.00,
    paid_amount: 700.00,
    patient_responsibility: 175.00,
    adjustment_reason: "CO-45"
  }
        │
        ▼
Field Mapper
  → Maps extracted fields to BC column schema
  → Formats dates, amounts to BC-compatible format
  → Validates required fields
        │
        ▼
Excel Export (.xlsx)
  → Structured for BC Cash Receipt Journal
  → Ready for Edit-in-Excel import into Business Central
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core extraction logic |
| pdfplumber | Primary text layer extraction |
| PyMuPDF (fitz) | Fallback extraction for complex PDFs |
| Anthropic Claude API | Intelligent field identification and normalization |
| openpyxl | Excel output for BC import |
| python-dotenv | Environment management |

---

## Project Structure

```
pdf-eob-extractor/
├── src/
│   ├── extractor.py         # PDF text extraction (pdfplumber + PyMuPDF)
│   ├── parser.py            # Claude API field extraction
│   ├── mapper.py            # BC field mapping and formatting
│   ├── exporter.py          # Excel output generation
│   └── validator.py         # Required field validation
├── sample_output/
│   └── bc_import_template.xlsx   # Example BC Cash Receipt format
├── .env.example
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/pranay-eligeti/pdf-eob-extractor.git
cd pdf-eob-extractor
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
```

### 4. Run extraction
```bash
python src/extractor.py --input path/to/eob.pdf --output output/bc_import.xlsx
```

---

## Environment Variables

```env
# .env.example
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OUTPUT_DIR=./output
```

---

## Requirements

```
pdfplumber>=0.10.0
PyMuPDF>=1.23.0
anthropic>=0.25.0
openpyxl>=3.1.0
python-dotenv>=1.0.0
```

---

## Business Central Import

The output Excel file is structured for the **Cash Receipt Journal** in BC:

| BC Field | Source |
|----------|--------|
| Document No. | Claim Number |
| Posting Date | Service Date |
| Account No. | Payer Code |
| Description | Patient Name + Claim |
| Amount | Paid Amount |
| Applies-to Doc. | Invoice Reference |

Import via: **Business Central → Cash Receipt Journal → Edit in Excel → Upload**

---

## Author

**Pranay Eligeti** — [linkedin.com/in/pranay-eligeti](https://linkedin.com/in/pranay-eligeti)
