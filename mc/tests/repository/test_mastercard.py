import json
import unittest

import httpretty
from requests import HTTPError

from repository import mastercard
import pytest


@httpretty.activate
class TestMastercardSettle(unittest.TestCase):
    def test_success(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://www.mastercard.com/settlement/currencyrate/conversion-rate?fxDate=2018-06-03&transCurr=USD&crdhldBillCurr=GBP&bankFee=0&transAmt=10',
            self.valid_response(),
        )

        result = mastercard.settle(
            bank_fee_percentage=0,
            card_currency='GBP',
            exchange_rate_date='2018-06-03',
            transaction_amount=10,
            transaction_currency='USD',
        )

        assert result['crdhldBillAmt'] == 7.54287

    def test_throws_on_bad_status(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://www.mastercard.com/settlement/currencyrate/conversion-rate?fxDate=2018-06-03&transCurr=USD&crdhldBillCurr=GBP&bankFee=0&transAmt=10',
            status=400
        )

        with pytest.raises(HTTPError):
            mastercard.settle(
                bank_fee_percentage=0,
                card_currency='GBP',
                exchange_rate_date='2018-06-03',
                transaction_amount=10,
                transaction_currency='USD',
            )

    @staticmethod
    def valid_response():
        return json.dumps({
            "name": "settlement-conversion-rate",
            "description": "Settlement conversion rate and billing amount",
            "date": "2018-06-03 16:03:19",
            "data": {
                "conversionRate": 0.754287,
                "crdhldBillAmt": 7.542870,
                "fxDate": "2018-06-03",
                "transCurr": "USD",
                "crdhldBillCurr": "GBP",
                "transAmt": 10,
            }
        })


@httpretty.activate
class TestMastercardRatesAvailable(unittest.TestCase):
    def test_success_true(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://www.mastercard.com/settlement/currencyrate/conversion-rate-issued?date=2018-06-03',
            self.valid_response('YES'),
        )

        result = mastercard.rates_available('2018-06-03')

        assert result

    def test_success_false(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://www.mastercard.com/settlement/currencyrate/conversion-rate-issued?date=2018-06-03',
            self.valid_response('NO'),
        )

        result = mastercard.rates_available('2018-06-03')

        assert not result

    def test_throws_on_bad_status(self):
        httpretty.register_uri(
            httpretty.GET,
            'https://www.mastercard.com/settlement/currencyrate/conversion-rate-issued?date=2018-06-03',
            status=400
        )

        with pytest.raises(HTTPError):
            mastercard.rates_available('2018-06-03')

    @staticmethod
    def valid_response(rate_issued):
        return json.dumps({
            "name": "settlement-conversion-rate-issued",
            "description": "Is settlement conversion rate issued",
            "date": "2018-06-03 16:02:25",
            "data": {
                "rateIssued": rate_issued
            }
        })


class TestMastercardCurrenciesAvailable(unittest.TestCase):
    def valid_response(self):
        return json.dumps({
            "name": "settlement-currency",
            "description": "A list of settlement active currencies",
            "date": "2018-06-03 16:02:25",
            "data": {
                "currencies": [
                    {"alphaCd": "AFN", "currNam": "AFGHANISTAN AFGHANI "},
                    {"alphaCd": "ALL", "currNam": "ALBANIAN LEK"},
                    {"alphaCd": "DZD", "currNam": "ALGERIAN DINAR      "},
                    {"alphaCd": "AOA", "currNam": "ANGOLAN KWANZA"},
                    {"alphaCd": "ARS", "currNam": "ARGENTINE PESO"},
                    {"alphaCd": "AMD", "currNam": "ARMENIAN DRAM       "},
                    {"alphaCd": "AWG", "currNam": "ARUBAN GUILDER"},
                    {"alphaCd": "AUD", "currNam": "AUSTRALIAN DOLLAR"},
                    {"alphaCd": "AZN", "currNam": "AZERBAIJAN MANAT"},
                    {"alphaCd": "BSD", "currNam": "BAHAMIAN DOLLAR     "},
                    {"alphaCd": "BHD", "currNam": "BAHRAIN DINAR"},
                    {"alphaCd": "BDT", "currNam": "BANGLADESH TAKA     "},
                    {"alphaCd": "BBD", "currNam": "BARBADOS DOLLAR     "},
                    {"alphaCd": "BYN", "currNam": "BELARUSSIAN RUBLE"},
                    {"alphaCd": "BZD", "currNam": "BELIZE DOLLAR       "},
                    {"alphaCd": "BMD", "currNam": "BERMUDAN DOLLAR     "},
                    {"alphaCd": "BTN", "currNam": "BHUTANESE NGULTRUM  "},
                    {"alphaCd": "BOB", "currNam": "BOLIVIAN BOLIVIANO"},
                    {"alphaCd": "BAM",
                     "currNam": "BOSNIAN CONVERTIBLE MARK"},
                    {"alphaCd": "BWP", "currNam": "BOTSWANA PULA       "},
                    {"alphaCd": "BRL", "currNam": "BRAZILIAN REAL"},
                    {"alphaCd": "BND", "currNam": "BRUNEI DOLLAR       "},
                    {"alphaCd": "BIF", "currNam": "BURUNDI FRANC       "},
                    {"alphaCd": "XOF", "currNam": "C.F.A. FRANC BCEAO  "},
                    {"alphaCd": "XAF", "currNam": "C.F.A. FRANC BEAC   "},
                    {"alphaCd": "XPF", "currNam": "C.F.P. FRANC"},
                    {"alphaCd": "KHR", "currNam": "CAMBODIA RIEL       "},
                    {"alphaCd": "CAD", "currNam": "CANADIAN DOLLAR"},
                    {"alphaCd": "CVE", "currNam": "CAPE VERDE ESCUDO   "},
                    {"alphaCd": "KYD", "currNam": "CAYMAN ISL DOLLAR   "},
                    {"alphaCd": "CLP", "currNam": "CHILEAN PESO"},
                    {"alphaCd": "CNY", "currNam": "CHINA YUAN RENMINBI "},
                    {"alphaCd": "COP", "currNam": "COLOMBIAN PESO      "},
                    {"alphaCd": "KMF", "currNam": "COMOROS FRANC       "},
                    {"alphaCd": "CDF", "currNam": "CONGOLESE FRANC     "},
                    {"alphaCd": "CRC", "currNam": "COSTA RICAN COLON   "},
                    {"alphaCd": "HRK", "currNam": "CROATIAN KUNA"},
                    {"alphaCd": "CUP", "currNam": "CUBAN PESO          "},
                    {"alphaCd": "CZK", "currNam": "CZECH KORUNA"},
                    {"alphaCd": "DKK", "currNam": "DANISH KRONE"},
                    {"alphaCd": "DJF", "currNam": "DJIBOUTI FRANC      "},
                    {"alphaCd": "DOP", "currNam": "DOMINICAN PESO"},
                    {"alphaCd": "XCD", "currNam": "E. CARIBBEAN D LR   "},
                    {"alphaCd": "EGP", "currNam": "EGYPTIAN POUND"},
                    {"alphaCd": "SVC", "currNam": "EL SALVADOR COLON   "},
                    {"alphaCd": "ETB", "currNam": "ETHIOPEAN BIRR      "},
                    {"alphaCd": "EUR", "currNam": "EURO"},
                    {"alphaCd": "FKP", "currNam": "FALKLAND ISL POUND  "},
                    {"alphaCd": "FJD", "currNam": "FIJI DOLLAR         "},
                    {"alphaCd": "GMD", "currNam": "GAMBIA DALASI       "},
                    {"alphaCd": "GEL", "currNam": "GEORGIAN LARI"},
                    {"alphaCd": "GHS", "currNam": "GHANAIAN CEDI"},
                    {"alphaCd": "GIP", "currNam": "GIBRALTAR POUND     "},
                    {"alphaCd": "GBP", "currNam": "GREAT BRITISH POUND"},
                    {"alphaCd": "GTQ", "currNam": "GUATEMALA QUETZAL   "},
                    {"alphaCd": "GNF", "currNam": "GUINEA FRANC        "},
                    {"alphaCd": "GYD", "currNam": "GUYANA DOLLAR       "},
                    {"alphaCd": "HTG", "currNam": "HAITI GOURDE        "},
                    {"alphaCd": "HNL", "currNam": "HONDURA LEMPIRA     "},
                    {"alphaCd": "HKD", "currNam": "HONG KONG DOLLAR"},
                    {"alphaCd": "HUF", "currNam": "HUNGARIAN FORINT"},
                    {"alphaCd": "ISK", "currNam": "ICELANDIC KRONA"},
                    {"alphaCd": "INR", "currNam": "INDIAN RUPEE"},
                    {"alphaCd": "IDR", "currNam": "INDONESIAN RUPIAH   "},
                    {"alphaCd": "IQD", "currNam": "IRAQI DINAR         "},
                    {"alphaCd": "ILS", "currNam": "ISRAELI SHEQEL"},
                    {"alphaCd": "JMD", "currNam": "JAMAICAN DOLLAR     "},
                    {"alphaCd": "JPY", "currNam": "JAPANESE YEN"},
                    {"alphaCd": "JOD", "currNam": "JORDANIAN DINAR     "},
                    {"alphaCd": "KZT", "currNam": "KAZAKHSTAN TENGE    "},
                    {"alphaCd": "KES", "currNam": "KENYAN SHILLING     "},
                    {"alphaCd": "KWD", "currNam": "KUWAITI DINAR       "},
                    {"alphaCd": "KGS", "currNam": "KYRGYZSTAN SOM      "},
                    {"alphaCd": "LAK", "currNam": "LAOTIAN KIP         "},
                    {"alphaCd": "LBP", "currNam": "LEBANESE POUND      "},
                    {"alphaCd": "LSL", "currNam": "LESOTHO LOTI        "},
                    {"alphaCd": "LRD", "currNam": "LIBERIAN DOLLAR"},
                    {"alphaCd": "LYD", "currNam": "LIBYAN DINAR        "},
                    {"alphaCd": "MOP", "currNam": "MACAU PATACA        "},
                    {"alphaCd": "MKD", "currNam": "MACEDONIAN DENAR    "},
                    {"alphaCd": "MGA", "currNam": "MALAGASCY ARIARY    "},
                    {"alphaCd": "MWK", "currNam": "MALAWI KWACHA       "},
                    {"alphaCd": "MYR", "currNam": "MALAYSIAN RINGGIT"},
                    {"alphaCd": "MVR", "currNam": "MALDIVE RUFIYAA     "},
                    {"alphaCd": "MRU", "currNam": "MAURITANIA OUGUIYA NEW"},
                    {"alphaCd": "MRO", "currNam": "MAURITANIA OUGUIYA OLD"},
                    {"alphaCd": "MUR", "currNam": "MAURITIUS RUPEE     "},
                    {"alphaCd": "MXN", "currNam": "MEXICAN PESO"},
                    {"alphaCd": "MDL", "currNam": "MOLDOVAN LEU        "},
                    {"alphaCd": "MNT", "currNam": "MONGOLIA TUGRIK     "},
                    {"alphaCd": "MAD", "currNam": "MOROCCAN DIRHAM"},
                    {"alphaCd": "MZN", "currNam": "MOZAMBIQUE METICAL  "},
                    {"alphaCd": "MMK", "currNam": "MYANMAR KYAT        "},
                    {"alphaCd": "NAD", "currNam": "NAMIBIA DOLLAR      "},
                    {"alphaCd": "NPR", "currNam": "NEPALESE RUPEE      "},
                    {"alphaCd": "ANG", "currNam": "NETH. ANT. GUILDER  "},
                    {"alphaCd": "BGN", "currNam": "NEW BULGARIAN LEV   "},
                    {"alphaCd": "NZD", "currNam": "NEW ZEALAND DOLLAR"},
                    {"alphaCd": "NIO", "currNam": "NICARAG CORDOBA ORO "},
                    {"alphaCd": "NGN", "currNam": "NIGERIAN NAIRA      "},
                    {"alphaCd": "NOK", "currNam": "NORWEGIAN KRONE"},
                    {"alphaCd": "OMR", "currNam": "OMAN RIAL           "},
                    {"alphaCd": "PKR", "currNam": "PAKISTAN RUPEE      "},
                    {"alphaCd": "PAB", "currNam": "PANAMA BALBOA       "},
                    {"alphaCd": "PGK", "currNam": "PAPUA NG KINA       "},
                    {"alphaCd": "PYG", "currNam": "PARAGUAY GUARANI    "},
                    {"alphaCd": "PEN", "currNam": "PERU NUEVO SOL      "},
                    {"alphaCd": "UYU", "currNam": "PESO URUGUAYO       "},
                    {"alphaCd": "PHP", "currNam": "PHILIPPINE PESO"},
                    {"alphaCd": "PLN", "currNam": "POLISH NEW ZLOTY    "},
                    {"alphaCd": "QAR", "currNam": "QATARI RIAL"},
                    {"alphaCd": "RON", "currNam": "ROMANIAN LEU"},
                    {"alphaCd": "RUB", "currNam": "RUSSIAN RUBLE       "},
                    {"alphaCd": "RWF", "currNam": "RWANDA FRANC        "},
                    {"alphaCd": "WST", "currNam": "SAMOA TALA          "},
                    {"alphaCd": "STN",
                     "currNam": "SAO TOME ANDPRINCIPE DOBRA NEW"},
                    {"alphaCd": "STD",
                     "currNam": "SAO TOME ANDPRINCIPE DOBRA OLD"},
                    {"alphaCd": "SAR", "currNam": "SAUDI RIYAL         "},
                    {"alphaCd": "RSD", "currNam": "SERBIAN DINAR"},
                    {"alphaCd": "SCR", "currNam": "SEYCHELLES RUPEE    "},
                    {"alphaCd": "SLL", "currNam": "SIERRA LEONE LEONE  "},
                    {"alphaCd": "SGD", "currNam": "SINGAPORE DOLLAR"},
                    {"alphaCd": "SBD", "currNam": "SOLOMON ISL DOLLAR  "},
                    {"alphaCd": "SOS", "currNam": "SOMALI SHILLING     "},
                    {"alphaCd": "ZAR", "currNam": "SOUTH AFRICAN RAND"},
                    {"alphaCd": "KRW", "currNam": "SOUTH KOREAN WON"},
                    {"alphaCd": "SSP", "currNam": "SOUTH SUDAN POUND   "},
                    {"alphaCd": "LKR", "currNam": "SRI LANKA RUPEE     "},
                    {"alphaCd": "SHP", "currNam": "ST. HELENA POUND    "},
                    {"alphaCd": "SRD", "currNam": "SURINAME DOLLAR     "},
                    {"alphaCd": "SZL", "currNam": "SWAZILAND LILANGENI "},
                    {"alphaCd": "SEK", "currNam": "SWEDISH KRONA"},
                    {"alphaCd": "CHF", "currNam": "SWISS FRANC         "},
                    {"alphaCd": "TWD", "currNam": "TAIWAN DOLLAR"},
                    {"alphaCd": "TJS", "currNam": "TAJIKISTAN SOMONI   "},
                    {"alphaCd": "TZS", "currNam": "TANZANIAN SHILLING  "},
                    {"alphaCd": "THB", "currNam": "THAI BAHT"},
                    {"alphaCd": "TOP", "currNam": "TONGA PAANGA        "},
                    {"alphaCd": "TTD", "currNam": "TRIN. & TOB. DOLLAR "},
                    {"alphaCd": "TND", "currNam": "TUNISIAN DINAR"},
                    {"alphaCd": "TRY", "currNam": "TURKISH LIRA        "},
                    {"alphaCd": "TMT", "currNam": "TURKMENISTAN MANAT  "},
                    {"alphaCd": "AED", "currNam": "UAE DIRHAM          "},
                    {"alphaCd": "UGX", "currNam": "UGANDA SHILLING     "},
                    {"alphaCd": "UAH", "currNam": "UKRAINIAN HRYVNIA"},
                    {"alphaCd": "USD", "currNam": "UNITED STATES DOLLAR"},
                    {"alphaCd": "UZS", "currNam": "UZBEKISTAN SUM      "},
                    {"alphaCd": "VUV", "currNam": "VANUATU VATU        "},
                    {"alphaCd": "VEF", "currNam": "VENEZ BOLIVAR FUERTE"},
                    {"alphaCd": "VND", "currNam": "VIETNAM DONG"},
                    {"alphaCd": "YER", "currNam": "YEMENI RIAL         "},
                    {"alphaCd": "ZMW", "currNam": "ZAMBIAN KWACHA      "}
                ]
            }
        })
