MasterCard Currency Converter
=============================

Command line interface to MasterCard currency conversions.

It uses the currencies as can be found in the [MasterCard Currency Conversion Tool](https://www.mastercard.com/global/currencyconversion/index.html).

## Installation

1.  Clone the repository.
2.  Install the script's dependencies:

    Linux:
    ```
    python3 -m pip install --user pipenv
    pipenv install
    pipenv run ...
    ```

    Windows:
    ```
    py -3 -m pip install --user pipenv
    pipenv install
    pipenv run ...
    ```

## Usage

To use it, simply call the script with the amount you're converting, and the currency before and after.

For example, if I had paid 10 US Dollars and wanted to know how much that was in British Pound Sterling:

```shell
Linux:
python2 mastercardConvert.py --recent 10 USD GBP

Windows:
py mastercardConvert.py --recent 10 USD GBP
```

## Development

This project uses `python3`.

This project uses `pipenv` to isolate its environment.  Install it with:

```bash
python3 -m pip install --user pipenv
```

Then install the project's dependencies:

```bash
pipenv install
```

Use `pipenv run` to run commands inside the virtualenv from outside the virtualenv.
Use `pipenv shell` to get a shell inside the virtualenv.

## Known issues

MasterCard don't tend to publish today's exchange rates until part way through the day; this is also affected by your time zone.  This means that sometimes the exchange rates for today might not be available.  If this happens to you, try `--yesterday`.  While it means that the exchange rates my not accurately reflect what is used in your transaction, the differences tend to be small.

MasterCard don't publish new exchange rates on Saturdays or Sundays.  Not much I can do there!
