# Check Balance
Check your Euros balance.


## Authenticate

[Start a new API session](authenticate.md) and grab the ``auth_token`` from the response payload. You will pass the authentication token to all other endpoints via the ``X-Auth-Token`` header.


## Check Balances

To find out how many Euros you have, call the **Get Balance** endpoint, passing "EUR" as the third URI path parameter.

``GET /v2/balances/EUR``

| Parameter Name   | Parameter Type | Example Value                        |
| ---------------- | -------------- | ------------------------------------ |
| ``X-Auth-Token`` | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

The following response shows that you hold 15,458.12 Euros in your Currencycloud account.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
    "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
    "currency": "EUR",
    "amount": "250.00",
    "created_at": "2017-12-10T16:05:20+00:00",
    "updated_at": "2017-12-10T16:05:20+00:00"
}
```

Alternatively, you can check the balances for all currencies held in your Currencycloud account, or any sub-account, by calling the **Find Balances** endpoint.

``GET /v2/balances/find``

| Parameter Name   | Parameter Type | Example Value                        |
| ---------------- | -------------- | ------------------------------------ |
| ``X-Auth-Token`` | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |


Example response:

```
{
    "balances": [
        {
            "id": "c52128a4-3918-40dc-a92a-7225cef3a4a6",
            "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
            "currency": "GBP",
            "amount": "10750.00",
            "created_at": "2017-12-10T16:05:19+00:00",
            "updated_at": "2017-12-10T16:05:19+00:00"
        },
        {
            "id": "349a2b87-9455-4808-9e68-515daf1f7298",
            "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
            "currency": "USD",
            "amount": "550.00",
            "created_at": "2017-12-10T16:05:19+00:00",
            "updated_at": "2017-12-10T16:05:19+00:00"
        },
        {
            "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
            "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
            "currency": "EUR",
            "amount": "250.00",
            "created_at": "2017-12-10T16:05:20+00:00",
            "updated_at": "2017-12-10T16:05:20+00:00"
        }
    ],
    "pagination": {
        "total_entries": 3,
        "total_pages": 1,
        "current_page": 1,
        "per_page": 25,
        "previous_page": -1,
        "next_page": -1,
        "order": "created_at",
        "order_asc_desc": "asc"
    }
}
```


## Next Step

[Buy more Euros using funds from your Pound Sterling balance.](convert.md)
