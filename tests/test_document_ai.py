from pathlib import Path

from src.extractor import read_fixture
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
