#!/usr/bin/env python

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



# Parse arguments
parser = argparse.ArgumentParser(description="Convert currency using MasterCard exchange rates")
parser.add_argument('from_quantity', type=float, help='Quantity of from_currency to convert to to_currency')
parser.add_argument('from_currency', help='The currency to convert from')
parser.add_argument('to_currency', help='The currency to convert to')
parser.add_argument('-d', '--date', help='Day the exchange was made in format MM/DD/YYYY. Only today and yesterday appear to be supported by MasterCard. Defaults to today', default=datetime.date.today().strftime('%m/%d/%Y'))
parser.add_argument('-x', '--debug', action='store_true', help='Displays debug information')
args = parser.parse_args()

# Currency codes are always uppercase
args.from_currency = string.upper(args.from_currency)
args.to_currency = string.upper(args.to_currency)


# Figure out URL
baseMasterCardUrl = 'https://www.mastercard.com/psder/eu/callPsder.do?service=getExchngRateDetails&baseCurrency={from_currency}&settlementDate={date}'
url = baseMasterCardUrl.format(from_currency=args.from_currency, date=args.date)

if args.debug:
	print url

# Parse from XML HTTP request
request = urllib2.urlopen(url)
xml = request.read()
request.close()

# Get currency exchange rates
currencies = parseMasterCardXML(xml)

if args.debug:
	for currency in currencies:
		print currencies[currency]


# Calculate conversion
to_quantity = args.from_quantity * currencies[args.to_currency]['rate']

# Output conversion
print to_quantity
