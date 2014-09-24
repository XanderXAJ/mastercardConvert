#!/usr/bin/env python
# For printing to stderr
from __future__ import print_function
from dateutil.parser import parse as parse_date



import argparse
import datetime
import xml.etree.ElementTree as ET
import sys
import string
import textwrap
import urllib2



DATE_FORMAT = '%m/%d/%Y'
MASTERCARD_URL = 'https://www.mastercard.com/psder/eu/callPsder.do?service=getExchngRateDetails&baseCurrency={from_currency}&settlementDate={date}'



# Reads a MasterCard XML string, returns a dictionary of currencies and their exchange rates,
# using their code (e.g. GBP, USD etc.) as the key.
def parseMasterCardXML(xml):
	root = ET.fromstring(xml)

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

	return currencies



# Parse command line arguments
parser = argparse.ArgumentParser(description="Convert currency using MasterCard exchange rates", epilog='If no date is specified, today\'s date is used.')
parser.add_argument('from_quantity', type=float, help='Quantity of from_currency to convert to to_currency')
parser.add_argument('from_currency', help='The currency to convert from, e.g. GBP, USD, JPY')
parser.add_argument('to_currency', help='The currency to convert to, e.g. GBP, USD, JPY')
parser.add_argument('-y', '--yesterday', action='store_true', help='Uses yesterday\'s exchange rates')
parser.add_argument('-d', '--date', help='Day the exchange was made in format MM/DD/YYYY. Only today and yesterday appear to be supported by MasterCard. Defaults to today')
parser.add_argument('-x', '--debug', action='store_true', help='Prints debug information to stderr')
args = parser.parse_args()

if args.debug:
	print(args, file=sys.stderr)

# Currency codes are always uppercase
args.from_currency = string.upper(args.from_currency)
args.to_currency = string.upper(args.to_currency)

# Figure out which date to use
# Date precedence goes: --date > --yesterday > today
if args.date is not None: # User-specified date
	args.date = parse_date(args.date).strftime(DATE_FORMAT)
elif args.yesterday: # Yesterday
	args.date = (datetime.date.today() - datetime.timedelta(days=1)).strftime(DATE_FORMAT)
else: # Today
	args.date = datetime.date.today().strftime(DATE_FORMAT)


# Figure out URL
url = MASTERCARD_URL.format(from_currency=args.from_currency, date=args.date)

if args.debug:
	print('MasterCard XML URL:', url, file=sys.stderr)

# Parse from XML HTTP request
request = urllib2.urlopen(url)
xml = request.read()
request.close()

# Get currency exchange rates
currencies = parseMasterCardXML(xml)

if args.debug:
	for currency in currencies:
		print(currencies[currency], file=sys.stderr)

# If no rates were returned, output an error message and exit
if len(currencies.keys()) == 0:
	print(textwrap.dedent('''\
		No currencies were returned from MasterCard.

		This tends to be for one of the following reasons:
			1) The exchange rates for today have yet to be published;
			2) The date used is a Saturday or Sunday;
			3) The date used is too far in the past;
			4) The to_currency does not exist in MasterCard's response.

		If the date used was today's and you got this message, try --yesterday.
		This may mean the exchange rate does not accurately reflect the transaction's,
		but differences tend to be small.
	'''), file=sys.stderr)
	sys.exit(1)

# If the specified to_currency does not exist, output an error message and exit
if args.to_currency not in currencies:
	print('Currency', args.to_currency, 'does not exist in MasterCard\'s response. Please check it exists.', file=sys.stderr)
	sys.exit(1)


# Calculate conversion
to_quantity = args.from_quantity * currencies[args.to_currency]['rate']

# Output conversion
print(to_quantity)
