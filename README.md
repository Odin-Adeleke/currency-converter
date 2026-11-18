# Currency Converter

A small command-line currency converter written in Python.

## Usage

```bash
python converter.py 100 CAD THB
```

Output:

```
100.00 CAD = 2,500.00 THB
```

## Rates

Rates are stored in `rates.json`, with USD as the base currency. The included rates are placeholders. Update them from a live source before using the converter for real decisions.

## Tests

```bash
python -m unittest test_converter
```

## Requirements

Python 3.8 or newer. No third-party packages.
