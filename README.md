MasterCard Currency Converter
=============================

Command line interface to MasterCard currency conversions.

It uses the currencies as can be found in the [MasterCard Currency Conversion Tool](https://www.mastercard.com/global/currencyconversion/index.html).

# How do I install it?

1. Clone the repository.
2. Install the script's dependencies

		pip install -r requirements.txt

# How do I use it?

To use it, simply call the script with the amount you're converting, and the currency before and after.

For example, if I had paid 10 US Dollars and wanted to know how much that was in British Pound Sterling:

```shell
python mastercardConvert.py 10 USD GBP
```

# Known issues

MasterCard don't tend to publish today's exchange rates until part way through the day; this is also affected by your time zone.  This means that sometimes the exchange rates for today might not be available.  If this happens to you, try `--yesterday`.  While it means that the exchange rates my not accurately reflect what is used in your transaction, the differences tend to be small.

MasterCard don't publish new exchange rates on Saturdays or Sundays.  Not much I can do there!
