#!/usr/bin/env python

import argparse
import logging
from functools import partial

from .domain import date, transaction


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Convert currency using MasterCard exchange rates",
        epilog="If no date is specified, the most recent date with rates is used.",
    )
    parser.add_argument(
        "from_quantity",
        type=float,
        help="Quantity of from_currency used in transaction",
    )
    parser.add_argument(
        "from_currency",
        type=str.upper,
        help="The currency to convert from, i.e. the transaction currency, case-insensitive, e.g. GBP, usd, JPY",
    )
    parser.add_argument(
        "to_currency",
        type=str.upper,
        help="The currency to convert to, i.e. the card currency, case-insensitive, e.g. GBP, usd, JPY",
    )
    parser.add_argument(
        "-d",
        "--date",
        help="Day the exchange was made in format YYYY-MM-DD. Only today and yesterday appear to be supported by MasterCard. Defaults to most recent day with rates.",
    )
    parser.add_argument(
        "--log-level",
        help="Set logging level",
        default="WARNING",
        type=str.upper,
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
    )
    parser.add_argument(
        "-t",
        "--today",
        action="store_true",
        help="Use today's exchange rates. This may error if today's rates have not been uploaded",
    )
    parser.add_argument(
        "-y",
        "--yesterday",
        action="count",
        default=0,
        help="Uses yesterday's exchange rates. Repeat to go further back in time",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.getLevelName(args.log_level))
    logging.debug(args)

    # Figure out which date to use
    if args.date is not None:  # User-specified date
        settle = partial(transaction.settle, exchange_rate_date=date.parse(args.date))
    elif args.today:  # Today
        settle = partial(transaction.settle, exchange_rate_date=date.date_today())
    elif (
        args.yesterday > 0
    ):  # Yesterday (note that yesterday can be specified multiple times)
        settle = partial(
            transaction.settle, exchange_rate_date=date.date_n_days_ago(args.yesterday)
        )
    else:  # Use most recent date with published rates, discover date from initial MasterCard call
        settle = transaction.settle_latest

    # Get card amount from MasterCard
    result = settle(
        transaction_amount=args.from_quantity,
        transaction_currency=args.from_currency,
        card_currency=args.to_currency,
    )

    # Output conversion
    print(result["card_amount"])
