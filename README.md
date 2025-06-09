# MasterCard Currency Converter

Command line interface to MasterCard currency conversions.

It uses the currencies as can be found in the [MasterCard Currency Conversion Tool](https://www.mastercard.com/global/currencyconversion/index.html).

## Requirements

This project uses [Python 3][python] & [pipx][pipx].

[pipx]: https://github.com/pypa/pipx
[python]: https://www.python.org/

## Installation

1. Clone the repository.
2. [Install pipx][pipx].
3. Install the project:

    ```shell
    pipx install .
    ```

4. Run the project:

    ```shell
    mc 10 USD GBP
    ```

## Usage

To use it, simply call the script with the amount you're converting, and the currency before and after.

For example, if I had paid 10 US Dollars and wanted to know how much that was in British Pound Sterling:

```shell
mc 10 USD GBP
```

## Development

For development, this project uses [Poetry][poetry] to isolate its environment.
You can install and manage it with [pipx][pipx] (recommended), or refer to [its instructions][poetry] for other options:

```bash
pipx install poetry
```

Then install the project's dependencies:

```bash
poetry install
```

Run the in-progress version of the code:

```bash
poetry run python -m mc 10 usd gbp
```

Note: `-m` is used to ensure imports work in the same way as they do when installing via `pipx`.

This project uses `unittest` for testing.
To run the tests:

```bash
poetry run python -m unittest
```

Use `poetry run` to run commands inside the virtualenv from outside the virtualenv.
Use `poetry shell` to get a shell inside the virtualenv.

[poetry]: https://python-poetry.org/

## Known issues

MasterCard don't tend to publish today's exchange rates until part way through the day; this is also affected by your time zone.  This means that sometimes the exchange rates for today might not be available.  If this happens, the script will automatically use yesterday's rates.  While it means that the exchange rates my not accurately reflect what is used in your transaction, the differences tend to be small.

MasterCard don't publish new exchange rates on Saturdays or Sundays.  Not much that can be done there!
