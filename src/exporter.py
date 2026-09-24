"""Excel export utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .mapper import BC_COLUMNS


def export_business_central(record: dict, output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([record], columns=BC_COLUMNS).to_excel(path, index=False)
    return path
