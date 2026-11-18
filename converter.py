"""Simple currency converter that uses a local rates file."""

import argparse
import json
from pathlib import Path

DEFAULT_RATES_FILE = Path(__file__).with_name("rates.json")


def load_rates(path=DEFAULT_RATES_FILE):
    """Return the rates dictionary (values are units per 1 base currency)."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["base"], data["rates"]


def convert(amount, from_currency, to_currency, rates, base="USD"):
    """Convert an amount between two currencies using base-currency rates."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    if from_currency not in rates:
        raise ValueError(f"Unknown currency: {from_currency}")
    if to_currency not in rates:
        raise ValueError(f"Unknown currency: {to_currency}")
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    amount_in_base = amount / rates[from_currency]
    return amount_in_base * rates[to_currency]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert between currencies.")
    parser.add_argument("amount", type=float, help="Amount to convert")
    parser.add_argument("from_currency", help="Currency code to convert from, e.g. CAD")
    parser.add_argument("to_currency", help="Currency code to convert to, e.g. THB")
    parser.add_argument("--rates", default=DEFAULT_RATES_FILE, help="Path to rates JSON file")
    args = parser.parse_args(argv)

    base, rates = load_rates(args.rates)
    result = convert(args.amount, args.from_currency, args.to_currency, rates, base)
    print(f"{args.amount:,.2f} {args.from_currency.upper()} = "
          f"{result:,.2f} {args.to_currency.upper()}")


if __name__ == "__main__":
    main()
