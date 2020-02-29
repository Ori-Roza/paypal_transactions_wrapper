from paypal_transactions_wrapper.exceptions import TransactionPropertyNotFound


class Transaction:
    KEY_MAP = {
        "TIMESTAMP": "date",
        "TIMEZONE": "timezone",
        "TYPE": "type",
        "EMAIL": "costumer_email",
        "NAME": "costumer_name",
        "TRANSACTIONID": "id",
        "STATUS": "status",
        "AMT": "amount",
        "CURRENCYCODE": "currency",
    }

    def __init__(self, transaction):
        self._transaction = transaction

    def __str__(self):
        return str(self._transaction)

    def __getattr__(self, item):
        if item in self._transaction:
            return self._transaction[item]
        raise TransactionPropertyNotFound("%s property has not found")