import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import compute_cash

D = pd.Timestamp("2026-09-01")
FX = pd.DataFrame({"rate_date": [D], "currency": ["USD"], "rate": [1.25]})


def deal(side, currency="USD", status="CONFIRMED"):
    return pd.DataFrame([dict(deal_date=D, product="BRENT", side=side, status=status,
                              quantity=1000, price=80.0, currency=currency, fee=32.0)])


class TestCash(unittest.TestCase):
    def test_sell_usd(self):
        self.assertAlmostEqual(compute_cash(deal("SELL"), FX).net_cash_eur[0], 63974.4)

    def test_buy_eur(self):
        self.assertAlmostEqual(compute_cash(deal("BUY", "EUR"), FX).net_cash_eur[0], -80032.0)

    def test_cancelled_ignored(self):
        self.assertTrue(compute_cash(deal("SELL", status="CANCELLED"), FX).empty)


if __name__ == "__main__":
    unittest.main()
