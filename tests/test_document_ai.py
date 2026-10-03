from pathlib import Path

from src.extractor import read_fixture
from src.extractor import extract_text
from src.exporter import export_business_central
from src.mapper import map_to_business_central
from src.parser import parse_deterministic
from src.validator import missing_required_fields, validate_business_central

ROOT = Path(__file__).resolve().parents[1]


def test_parse_synthetic_eob():
    text = read_fixture(ROOT / "sample_data" / "synthetic_eob.txt")
    record = parse_deterministic(text)
    assert record["claim_number"] == "CLM-DEMO-001"
    assert record["patient_name"] == "Alex Example"
    assert record["paid_amount"] == 700.0


def test_map_and_validate_business_central():
    record = parse_deterministic(read_fixture(ROOT / "sample_data" / "synthetic_eob.txt"))
    assert missing_required_fields(record) == []
    mapped = map_to_business_central(record)
    assert mapped["Document No."] == "CLM-DEMO-001"
    assert mapped["Amount"] == 700.0
    assert validate_business_central(mapped) == []


def test_zero_paid_amount_is_present():
    record = parse_deterministic(read_fixture(ROOT / "sample_data/synthetic_eob.txt"))
    record["paid_amount"] = 0.0
    assert missing_required_fields(record) == []
    assert validate_business_central(map_to_business_central(record)) == []
    record["paid_amount"] = None
    assert "paid_amount" in missing_required_fields(record)


def test_real_pdf_to_excel_offline(tmp_path):
    import fitz
    from openpyxl import load_workbook

    pdf = tmp_path / "synthetic.pdf"
    with fitz.open() as document:
        page = document.new_page()
        page.insert_text((72, 72), read_fixture(ROOT / "sample_data/synthetic_eob.txt"))
        document.save(pdf)
    record = parse_deterministic(extract_text(pdf))
    assert missing_required_fields(record) == []
    output = export_business_central(map_to_business_central(record), tmp_path / "synthetic.xlsx")
    workbook = load_workbook(output, read_only=True, data_only=True)
    try:
        rows = list(workbook.active.values)
        assert rows[1][0] == "CLM-DEMO-001"
        assert rows[1][4] == 700
    finally:
        workbook.close()
