import re
from paypal_transactions_wrapper.exceptions import *
from paypal_transactions_wrapper.connector import PayPalTransactionsConnector
from paypal_transactions_wrapper.transaction import Transaction


class PayPalTransactionsApi:
    COMPLETED_STATUS = "Completed"
    FAILED_STATUS = "Failed"
    PENDING_STATUS = "Pending"

    _LEN_THRESHOLD = 10000

    def __init__(self, api_username, api_password, api_signuature, http_timeout=300):
        try:
            self.__paypal_api = PayPalTransactionsConnector(
                api_username,
                api_password,
                api_signuature,
                http_timeout)

        except TransactionsConnectionError as error:
            raise TransactionsConfigError("Cannot connect Paypal, something wrong with the configuration details: %s" % error)

    @classmethod
    def __paypal_date_format(cls, date_st):
        return '%sT00:00:00Z' % date_st

    def __get_raw_transactions(self, **kwargs):
        """
        Using paypal library to get the raw entries.
        it is a bulk of attributes, each attribute ends with an index.
        :param kwargs:
        :return:
        """
        try:
            all_transactions = self.__paypal_api.get_transactions(**kwargs)
        except GetTransactionsError as error:
            raise GetTransactionsError("Cannot get all the transactions: %s" % error)

        return all_transactions

    def __parse_transactions(self, **kwargs):
        """
        each attribute ends with an index.
        we gather all the atts with the same index and create a Transcation object
        :param kwargs:
        :return: list of parsed transactions
        """
        try:
            raw_transactions = self.__get_raw_transactions(**kwargs)
        except GetTransactionsError:
            raise
        list_of_transactions = []

        transactions_dict = {}

        for t in raw_transactions:
            index = re.findall(r'\d+', t)  # getting the index
            if len(index) == 0:
                continue
            key = str(index[0])
            if key not in transactions_dict:
                transactions_dict[key] = {}

            transaction_property = t[2:len(t) - len(key)]  # extract the property name

            if len(raw_transactions[t]) == 0:
                att = ""
            else:
                att = raw_transactions[t][0]

            if transaction_property not in Transaction.KEY_MAP:
                transaction_key = transaction_property
            else:
                transaction_key = Transaction.KEY_MAP[transaction_property]

            transactions_dict[key][transaction_key] = att

        for t in transactions_dict:
            list_of_transactions.append(Transaction(transactions_dict[t]))

        return list_of_transactions

    def __filter_transactions(self, **kwargs):
        """
        Available statuses are:
            * All
            * Completed
            * Failed
            * Pending
        :param kwargs:
        :return:
        """
        status = kwargs["STATUS"]
        transactions = self.__parse_transactions(**kwargs)

        filtered = filter(lambda transaction: transaction.status == status, transactions)

        if len(transactions) > self._LEN_THRESHOLD:  # if too big, returns a generator
            return filtered

        return list(filtered)

    def _get_Completed_transactions(self, **kwargs):
        arguments = {"STATUS": self.COMPLETED_STATUS}
        arguments.update(kwargs)
        return self.__filter_transactions(**arguments)

    def _get_Pending_transactions(self, **kwargs):
        arguments = {"STATUS": self.PENDING_STATUS}
        arguments.update(kwargs)
        return self.__filter_transactions(**arguments)

    def _get_Failed_transactions(self, **kwargs):
        arguments = {"STATUS": self.FAILED_STATUS}
        arguments.update(kwargs)
        return self.__parse_transactions(**arguments)

    def _get_statuses(self):
        return [att for att in dir(self) if att.endswith("_STATUS")]

    def __check_status_exists(self, status):
        status = [valid_status for valid_status in self._get_statuses() if status.lower() in valid_status.lower()]
        return len(status) == 1

    def __get_transaction_func_by_status(self, status):
        if not self.__check_status_exists(status):
            raise TransactionStatusNotFound("%s is not a valid status" % status)
        return getattr(self, "_get_%s_transactions" % status)

    def get_transactions(self, start=None, status=None):
        if status is None:
            transaction_status = self.COMPLETED_STATUS
        else:
            transaction_status = status

        transaction_by_status = self.__get_transaction_func_by_status(transaction_status)

        return transaction_by_status(STARTDATE=self.__paypal_date_format('1980-01-01' if not start else start))

    def get_transactions_between_dates(self, start, end, status=None):
        if status is None:
            transaction_status = self.COMPLETED_STATUS
        else:
            transaction_status = status

        transaction_by_status = self.__get_transaction_func_by_status(transaction_status)

        return transaction_by_status(STARTDATE=self.__paypal_date_format(start), ENDDATE=self.__paypal_date_format(end))