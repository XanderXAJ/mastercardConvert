#!/usr/bin/env python2
# For printing to stderr
from __future__ import print_function

import argparse
import datetime
import string
import sys
import textwrap
import xml.etree.ElementTree as ET

import requests
from dateutil.parser import parse as parse_date

DATE_FORMAT = '%m/%d/%Y'
MASTERCARD_INIT_URL = 'https://www.mastercard.com/psder/eu/callPsder.do?service=loadInitialValues'
MASTERCARD_RATE_URL = 'https://www.mastercard.com/psder/eu/callPsder.do?service=getExchngRateDetails&baseCurrency={from_currency}&settlementDate={date}'


def makeMasterCardRequest(url, verbosity=0):
    if verbosity >= 1:
        print('Request URL:', url, file=sys.stderr)

    # Parse from XML HTTP request
    request = requests.get(url)
    xml = request.text

    if verbosity >= 3:
        print(xml, file=sys.stderr);

    # Get currency exchange rates
    currencies, settlement_date = parseMasterCardXML(xml)

    if verbosity >= 2:
        print('Settlement date:', settlement_date, file=sys.stderr)
        for currency in currencies:
            print(currencies[currency], file=sys.stderr)

    return currencies, settlement_date


# Reads a MasterCard XML string, returns a dictionary of currencies and their exchange rates,
# using their code (e.g. GBP, USD etc.) as the key.
def parseMasterCardXML(xml):
    root = ET.fromstring(xml)

    # Get settlement date of excahnge rates
    settlement_date = root.findtext('./SETTLEMENT_DATE')

    # Get all currency elements
    xmlCurrencies = root.findall('./TRANSACTION_CURRENCY/')

    # Extract currency info from XML
    currencies = {}

    for xmlCurrency in xmlCurrencies:
        currency = {
            'code': xmlCurrency.find('ALPHA_CURENCY_CODE').text,
            'name': xmlCurrency.find('CURRENCY_NAME').text,
            'rate': float(xmlCurrency.find('CONVERSION_RATE').text)
        }

        # Store currencies so they are looked up by their key
        currencies[currency['code']] = currency

    return currencies, settlement_date


# Parse command line arguments
parser = argparse.ArgumentParser(description="Convert currency using MasterCard exchange rates",
                                 epilog='Dates are used in the following order: --date, --recent, --yesterday, today')
parser.add_argument('from_quantity', type=float, help='Quantity of from_currency to convert to to_currency')
parser.add_argument('from_currency', type=string.upper, help='The currency to convert from, e.g. GBP, USD, JPY')
parser.add_argument('to_currency', type=string.upper, help='The currency to convert to, e.g. GBP, USD, JPY')
parser.add_argument('-d', '--date',
                    help='Day the exchange was made in format MM/DD/YYYY. Only today and yesterday appear to be supported by MasterCard. Defaults to today')
parser.add_argument('-r', '--recent', action='store_true', default=True,
                    help='Use most recent date that exchange rates are available for (default)')
parser.add_argument('-v', '--verbosity', action='count',
                    help='Increases output verbosity; specify multiple times for more')
parser.add_argument('-t', '--today', action='store_true',
                    help='Use today\'s exchange rates. This may error if today\' rates have not been uploaded')
parser.add_argument('-y', '--yesterday', action='count',
                    help='Uses yesterday\'s exchange rates. Repeat to go further back in time')
args = parser.parse_args()

if args.verbosity >= 1:
    print(args, file=sys.stderr)

# Figure out which date to use
# Date precedence goes: --date > --yesterday > today
if args.date is not None:  # User-specified date
    args.date = parse_date(args.date).strftime(DATE_FORMAT)
elif args.today:  # Today
    _, args.date = makeMasterCardRequest(MASTERCARD_INIT_URL, verbosity=args.verbosity)
elif args.yesterday > 0:  # Yesterday
    args.date = (datetime.date.today() - datetime.timedelta(days=args.yesterday)).strftime(DATE_FORMAT)
else:  # Use most recent date with published rates, discover date from initial MasterCard call
    args.date = datetime.date.today().strftime(DATE_FORMAT)

# Get exchange rates from MasterCard
url = MASTERCARD_RATE_URL.format(from_currency=args.from_currency, date=args.date)
currencies, settlement_date = makeMasterCardRequest(url, verbosity=args.verbosity)

# If no rates were returned, output an error message and exit
if len(currencies.keys()) == 0:
    print(textwrap.dedent('''\
        No currencies were returned from MasterCard.

        This tends to be for one of the following reasons:
            1) The exchange rates for today have yet to be published;
            2) The date used is a Saturday or Sunday;
            3) The date used is too far in the past;
            4) The from_currency does not exist in MasterCard's response.

        To get the most recent exchange rates that MasterCard released, try --recent.
        This may mean the exchange rate does not accurately reflect the transaction's,
        but differences tend to be small.
    '''), file=sys.stderr)
    sys.exit(1)

# If the specified to_currency does not exist, output an error message and exit
if args.to_currency not in currencies:
    print(textwrap.dedent('''\
        Currency {currency} does not exist in MasterCard\'s response. Please check it exists.

        You can confirm the supported currencies by visiting the following URL:
        https://www.mastercard.com/global/currencyconversion/index.html
    '''.format(currency=args.to_currency)), file=sys.stderr)
    sys.exit(1)

# Calculate conversion
to_quantity = args.from_quantity * currencies[args.to_currency]['rate']

# Output conversion
print(to_quantity)
