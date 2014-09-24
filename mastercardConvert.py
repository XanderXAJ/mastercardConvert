#!/usr/bin/env python
# For printing to stderr
from __future__ import print_function



import argparse
import datetime
import xml.etree.ElementTree as ET
import sys
import string
import urllib2



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
	# TODO: parse date
	print('TODO', file=sys.stderr)
elif args.yesterday: # Yesterday
	args.date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%m/%d/%Y')
else: # Today
	args.date = datetime.date.today().strftime('%m/%d/%Y')


# Figure out URL
baseMasterCardUrl = 'https://www.mastercard.com/psder/eu/callPsder.do?service=getExchngRateDetails&baseCurrency={from_currency}&settlementDate={date}'
url = baseMasterCardUrl.format(from_currency=args.from_currency, date=args.date)

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


# Calculate conversion
to_quantity = args.from_quantity * currencies[args.to_currency]['rate']

# Output conversion
print(to_quantity)
