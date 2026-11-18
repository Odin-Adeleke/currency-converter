"""Simple currency converter with local or live exchange rates."""

import argparse
import json
import urllib.request
from pathlib import Path

DEFAULT_RATES_FILE = Path(__file__).with_name("rates.json")
LIVE_RATES_URL = "https://open.er-api.com/v6/latest/USD"


def load_rates(path=DEFAULT_RATES_FILE):
    """Return (base, rates) from a local JSON file."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["base"], data["rates"]


def parse_rates_payload(payload):
    """Return (base, rates) from a live API response, or raise ValueError."""
    if payload.get("result") != "success":
        raise ValueError("Live rates response was not successful")
    base = payload.get("base_code")
    rates = payload.get("rates")
    if not base or not isinstance(rates, dict) or not rates:
        raise ValueError("Live rates response is missing data")
    return base, rates


def fetch_live_rates(url=LIVE_RATES_URL, timeout=10):
    """Fetch (base, rates) from the live API. Raises on network or data errors."""
    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_rates_payload(payload)


def convert(amount, from_currency, to_currency, rates):
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
    parser.add_argument("--rates", default=DEFAULT_RATES_FILE, help="Path to local rates JSON file")
    parser.add_argument("--live", action="store_true", help="Use live rates, falling back to the local file")
    args = parser.parse_args(argv)

    base, rates = load_rates(args.rates)
    if args.live:
        try:
            base, rates = fetch_live_rates()
            source = "live rates"
        except (OSError, ValueError) as error:
            print(f"Could not get live rates ({error}); using local rates.")
            source = "local rates"
    else:
        source = "local rates"

    result = convert(args.amount, args.from_currency, args.to_currency, rates)
    print(f"{args.amount:,.2f} {args.from_currency.upper()} = "
          f"{result:,.2f} {args.to_currency.upper()} ({source})")


if __name__ == "__main__":
    main()
