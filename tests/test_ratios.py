import unittest

from src.analytics.ratios import *


class TestRatios(unittest.TestCase):

    def test_net_profit_margin(self):
        self.assertEqual(net_profit_margin(100, 1000), 10)

    def test_net_profit_zero_sales(self):
        self.assertIsNone(net_profit_margin(100, 0))

    def test_roe(self):
        self.assertEqual(roe(100, 500, 500), 10)

    def test_negative_equity(self):
        self.assertIsNone(roe(100, -600, 100))

    def test_roce(self):
        self.assertEqual(roce(200, 500, 300, 200), 20)

    def test_roa(self):
        self.assertEqual(roa(100, 1000), 10)

    def test_zero_assets(self):
        self.assertIsNone(roa(100, 0))

    def test_opm(self):
        self.assertEqual(operating_profit_margin(150, 1000), 15)


if __name__ == "__main__":
    unittest.main()