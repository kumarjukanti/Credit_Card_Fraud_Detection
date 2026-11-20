import argparse
from pathlib import Path

from src.data.validate import validate_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    ingest = commands.add_parser("ingest", help="Validate a transaction CSV")
    ingest.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/creditcard.csv"),
        help="CSV path (default: %(default)s)",
    )
    args = parser.parse_args()

    try:
        validate_csv(args.input)
    except FileNotFoundError:
        ingest.exit(1, f"CSV not found: {args.input}\n")
    except (OSError, ValueError) as error:
        ingest.exit(1, f"Could not validate {args.input}: {error}\n")

    print(f"Validated {args.input}")


if __name__ == "__main__":
    main()
