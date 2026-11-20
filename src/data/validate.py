import csv
import math
from pathlib import Path

FEATURE_COLUMNS = ("Time", *(f"V{i}" for i in range(1, 29)), "Amount")
COLUMNS = (*FEATURE_COLUMNS, "Class")


def validate_csv(path: Path) -> None:
    """Raise ValueError if the CSV violates the dataset contract."""
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream)
        if next(reader, None) != list(COLUMNS):
            raise ValueError("Expected the Kaggle creditcard.csv column header")

        row_number = 1
        for row_number, row in enumerate(reader, start=2):
            if len(row) != len(COLUMNS):
                raise ValueError(f"Row {row_number}: expected {len(COLUMNS)} fields")
            if row[-1] not in {"0", "1"}:
                raise ValueError(f"Row {row_number}: Class must be 0 or 1")

            for column, value in zip(FEATURE_COLUMNS, row[:-1], strict=True):
                try:
                    number = float(value)
                except ValueError as error:
                    raise ValueError(
                        f"Row {row_number}: {column} must be numeric"
                    ) from error
                if not math.isfinite(number):
                    raise ValueError(f"Row {row_number}: {column} must be finite")

        if row_number == 1:
            raise ValueError("Expected at least one transaction")
