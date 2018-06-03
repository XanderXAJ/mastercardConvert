import logging
import string

import requests

CURRENCY_URL = 'https://www.mastercard.us/settlement/currencyrate/settlement-currencies'
RATE_URL = string.Template(
    'https://www.mastercard.us/settlement/currencyrate/fxDate=$exchange_rate_date;transCurr=$transaction_currency;crdhldBillCurr=$card_currency;bankFee=$bank_fee_percentage;transAmt=$transaction_amount/conversion-rate')
RATE_ISSUED_URL = string.Template(
    'https://www.mastercard.us/settlement/currencyrate/conversion-rate-issued?date=$exchange_rate_date')
REFERRER_URL = 'https://www.mastercard.us/en-us/consumers/get-support/convert-currency.html'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:59.0) Gecko/20100101 Firefox/59.0'


def settle(transaction_amount, transaction_currency, card_currency, exchange_rate_date, bank_fee_percentage):
    url = RATE_URL.substitute(
        bank_fee_percentage=bank_fee_percentage,
        card_currency=card_currency,
        exchange_rate_date=exchange_rate_date,
        transaction_amount=transaction_amount,
        transaction_currency=transaction_currency,
    )

    response = make_mastercard_request(url)

    # Throw exception if a bad response code was returned
    response.raise_for_status()

    # Return just the 'data' key, as it is the only part of the request that contains relevant information
    json = response.json()
    logging.debug(json)

    return json['data']


def rates_available(exchange_rate_date):
    url = RATE_ISSUED_URL.substitute(
        exchange_rate_date=exchange_rate_date
    )

    response = make_mastercard_request(url)

    response.raise_for_status()

    return response.json()['data']['rateIssued'] == 'YES'


def make_mastercard_request(url):
    headers = {
        'Accept': 'application/json',
        'Referer': REFERRER_URL,
        'User-Agent': USER_AGENT,
    }

    return requests.get(
        url,
        headers=headers
    )
