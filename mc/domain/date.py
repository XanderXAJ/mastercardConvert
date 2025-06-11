import datetime

from dateutil.parser import parse as parse_date

MASTERCARD_DATE_FORMAT = "%Y-%m-%d"


def parse(date):
    return parse_date(date).strftime(MASTERCARD_DATE_FORMAT)


def date_today():
    return date_n_days_ago(0)


def date_yesterday():
    return date_n_days_ago(1)


def date_n_days_ago(days_ago):
    date = datetime.date.today() - datetime.timedelta(days=days_ago)
    return format_date(date)


def format_date(date):
    return date.strftime(MASTERCARD_DATE_FORMAT)
