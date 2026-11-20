import csv

import pytest

from src.data.validate import validate_csv


@pytest.mark.parametrize("label", ["0", "1", "2"])
def test_fraud_label_contract(tmp_path, label):
    path = tmp_path / "creditcard.csv"
    header = ["Time", *(f"V{i}" for i in range(1, 29)), "Amount", "Class"]
    row = ["10", *(["0.5"] * 28), "25.50", label]

    with path.open("w", encoding="utf-8", newline="") as stream:
        csv.writer(stream).writerows([header, row])

    if label == "2":
        with pytest.raises(ValueError, match="Class must be 0 or 1"):
            validate_csv(path)
    else:
        validate_csv(path)
