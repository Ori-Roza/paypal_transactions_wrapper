# **Paypal Transactions Wrapper**

creates an interface with Paypal Transactions API.


handles current statuses: Completed, Failed, Pending
`
connection = PayPalTransactionsApi(
                              api_username="XXX_api1.XXXX",
                              api_password="XXXXXX",
                              api_signuature="XXXXXXXXX",
                              )

transactions = connection.get_transactions(status="Completed")

transactions[0]

{   
    'date': '2020-02-28T23:32:07Z',
    'timezone': 'GMT',
    'type': 'Payment',
    'costumer_email': 'test@hotmail.com',
    'costumer_name': 'John Doe',
     'id': '123456789',
    'status': 'Completed',
    'amount': '30.00',
    'currency': 'USD',
    'FEEAMT': '-1.92',
    'NETAMT': '28.08',
 }


transactions = connection.get_transactions(start="1980-01-01", status="Failed")

transactions[0]

{   
    'date': '2020-02-28T23:32:07Z',
    'timezone': 'GMT',
    'type': 'Payment',
    'costumer_email': 'test@hotmail.com',
    'costumer_name': 'John Doe',
    'id': '123456789',
    'status': 'Failed',
    'amount': '30.00',
    'currency': 'USD',
 }


transactions = connection.get_transactions(start="2020-02-01" end="2020-02-02", status="Completed")

transactions[0]

{   
    'date': '2020-02-02T23:32:07Z',
    'timezone': 'GMT',
    'type': 'Payment',
    'costumer_email': 'test@hotmail.com',
    'costumer_name': 'John Doe',
    'id': '123456789',
    'status': 'Failed',
    'amount': '30.00',
    'currency': 'USD',
 }


If the list is too long, returns a generator.

`