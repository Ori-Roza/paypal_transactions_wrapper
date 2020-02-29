import requests
from urllib.parse import parse_qs
from paypal_transactions_wrapper.exceptions import TransactionsConnectionError


class PayPalTransactionsConnector:
    __VERSION__ = "98.0"
    __METHOD__ = "TransactionSearch"
    __URL__ = 'https://api-3t.paypal.com/nvp'

    def __init__(self, api_username, api_password, api_signature, http_timeout=300):
        self.__params = {"data": {},
                         "cert": None,
                         "url": self.__URL__,
                         "timeout": http_timeout,
                         "verify": True}

        self.__create_params(VERSION=self.__VERSION__,
                             METHOD = self.__METHOD__,
                             USER=api_username,
                             PWD=api_password,
                             SIGNATURE=api_signature)

        self.__transactions = {}

    def __create_params(self, **kwargs):
        self.__params["data"].update(kwargs)

    def __parse(self, response):
        try:
            self.__transactions = parse_qs(response)
        except ValueError as e:
            print(e)

    def __post(self):
        http_response = requests.post(**self.__params)
        if http_response.status_code > 399:
            raise TransactionsConnectionError("Connection error")
        self.__parse(http_response.text)

    def __make_handshake(self, status, start_date, end_date=None):
        self.__params["data"].update({"STATUS": status, "STARTDATE": start_date})

        if end_date:
            self.__params["data"].update({"ENDDATE": end_date})
        self.__post()

    def get_transactions(self, **kwargs):
        status = kwargs.get("STATUS", None)
        start_date = kwargs.get("STARTDATE", None)
        end_date = kwargs.get("ENDDATE", None)

        if not status or not start_date:
            raise ValueError("arguments are invalid")

        self.__make_handshake(status, start_date, end_date)
        return self.__transactions
