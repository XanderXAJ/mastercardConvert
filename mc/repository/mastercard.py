import logging
import string

import requests

from latest_user_agents import get_random_user_agent

CURRENCY_URL = (
    "https://www.mastercard.com/settlement/currencyrate/settlement-currencies"
)
RATE_URL = string.Template(
    "https://www.mastercard.com/settlement/currencyrate/conversion-rate?fxDate=$exchange_rate_date&transCurr=$transaction_currency&crdhldBillCurr=$card_currency&bankFee=$bank_fee_percentage&transAmt=$transaction_amount"
)
RATE_ISSUED_URL = string.Template(
    "https://www.mastercard.com/settlement/currencyrate/conversion-rate-issued?date=$exchange_rate_date"
)
REFERRER_URL = (
    "https://www.mastercard.com/global/en/personal/get-support/convert-currency.html"
)
HOST = "www.mastercard.com"


def settle(
    transaction_amount,
    transaction_currency,
    card_currency,
    exchange_rate_date,
    bank_fee_percentage,
):
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

    return json["data"]


def rates_available(exchange_rate_date):
    url = RATE_ISSUED_URL.substitute(exchange_rate_date=exchange_rate_date)

    response = make_mastercard_request(url)

    response.raise_for_status()

    return response.json()["data"]["rateIssued"] == "YES"


def make_mastercard_request(url):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": HOST,
        "Priority": "u=0",
        "Referer": REFERRER_URL,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1",
        "User-Agent": get_random_user_agent(),
    }

    logging.debug(f"Making request to Mastercard API: {url}")
    logging.debug(f"Using headers: {headers}")

    return requests.get(url, headers=headers)
