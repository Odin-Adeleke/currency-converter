import unittest

from converter import convert, parse_rates_payload

RATES = {"USD": 1.0, "CAD": 1.37, "THB": 34.25}


class ConvertTests(unittest.TestCase):
    def test_same_currency_returns_same_amount(self):
        self.assertAlmostEqual(convert(100, "CAD", "CAD", RATES), 100)

    def test_usd_to_cad(self):
        self.assertAlmostEqual(convert(10, "USD", "CAD", RATES), 13.7)

    def test_cad_to_thb(self):
        self.assertAlmostEqual(convert(100, "cad", "thb", RATES), 100 / 1.37 * 34.25)

    def test_unknown_currency_raises(self):
        with self.assertRaises(ValueError):
            convert(10, "XYZ", "CAD", RATES)

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            convert(-5, "USD", "CAD", RATES)


class LiveRatesTests(unittest.TestCase):
    def test_parses_successful_payload(self):
        payload = {"result": "success", "base_code": "USD", "rates": {"USD": 1, "CAD": 1.37}}
        base, rates = parse_rates_payload(payload)
        self.assertEqual(base, "USD")
        self.assertEqual(rates["CAD"], 1.37)

    def test_rejects_failed_payload(self):
        with self.assertRaises(ValueError):
            parse_rates_payload({"result": "error"})

    def test_rejects_missing_rates(self):
        with self.assertRaises(ValueError):
            parse_rates_payload({"result": "success", "base_code": "USD"})


if __name__ == "__main__":
    unittest.main()
