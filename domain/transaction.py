import datetime
import logging

import repository.mastercard as mastercard
from domain import date

DATE_FORMAT = '%Y-%m-%d'


def settle(transaction_amount, transaction_currency, card_currency, exchange_rate_date, bank_fee_percentage=0):
    result = mastercard.settle(
        bank_fee_percentage=bank_fee_percentage,
        card_currency=card_currency,
        exchange_rate_date=exchange_rate_date,
        transaction_amount=transaction_amount,
        transaction_currency=transaction_currency,
    )

    logging.debug(result)

    return {
        "bank_fee_percentage": bank_fee_percentage,
        "card_amount": result["crdhldBillAmt"],
        "card_currency": result["crdhldBillCurr"],
        "conversion_rate": result["conversionRate"],
        "conversion_rate_date": result["fxDate"],
        "transaction_amount": result["transAmt"],
        "transaction_currency": result["transCurr"],
    }


def settle_latest(transaction_amount, transaction_currency, card_currency, bank_fee_percentage=0):
    date_today = date.date_today()
    if mastercard.rates_available(date_today):
        exchange_rate_date = date_today
    else:
        exchange_rate_date = date.date_yesterday()

    return settle(transaction_amount, transaction_currency, card_currency, exchange_rate_date, bank_fee_percentage)
