import unittest
from unittest.mock import patch

from domain import transaction


class TestTransactionSettle(unittest.TestCase):
    @patch('mc.repository.mastercard.settle')
    def test_success_return(self, settle_mock):
        settle_mock.return_value = self.valid_settle_return_value()

        result = transaction.settle(
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

        self.assertEqual(result, {
            'bank_fee_percentage': 0,
            'card_amount': 7.542870,
            'card_currency': 'GBP',
            'conversion_rate': 0.754287,
            'conversion_rate_date': '2018-06-03',
            'transaction_amount': 10,
            'transaction_currency': 'USD',
        })

    @patch('mc.repository.mastercard.settle')
    def test_success_call(self, settle_mock):
        settle_mock.return_value = self.valid_settle_return_value()

        transaction.settle(
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

        settle_mock.assert_called_once_with(
            bank_fee_percentage=0,
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

    @patch('mc.repository.mastercard.settle')
    def test_success_call_with_bank_fee(self, settle_mock):
        settle_mock.return_value = self.valid_settle_return_value()

        transaction.settle(
            bank_fee_percentage=5,
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

        settle_mock.assert_called_once_with(
            bank_fee_percentage=5,
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

    @staticmethod
    def valid_settle_return_value():
        return {
            "conversionRate": 0.754287,
            "crdhldBillAmt": 7.542870,
            "fxDate": "2018-06-03",
            "transCurr": "USD",
            "crdhldBillCurr": "GBP",
            "transAmt": 10,
            "bankFee": 0
        }
