# Settle
Before conversions can be processed, you must create a settlement.


## Authenticate

[Start a new API session](authenticate.md) and grab the ``auth_token`` from the response payload. You will pass the authentication token to all other endpoints via the ``X-Auth-Token`` header.


## Create Settlement

``POST /v2/settlements/create`` \
``Content-Type: multipart/form-data``

| Parameter Name   | Parameter Type | Example Value                        |
| ---------------- | -------------- | ------------------------------------ |
| ``X-Auth-Token`` | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

On success, the response payload will contain full details of the settlement as recorded against your Currencycloud account, including a unique ID for the settlement.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "a937f05e-e9fd-442e-a46f-11e84ba37806",
    "short_reference": "20140101-BCDFGH",
    "status": "open",
    "conversion_ids": [],
    "entries": {},
    "created_at": "2018-02-02T12:15:05+00:00",
    "updated_at": "2018-02-02T12:15:05+00:00",
    "released_at": "2018-02-02T12:15:05+00:00"
}
```


## Add Conversion to Settlement
In a [previous step](convert.md) you created a conversion of GBP 8,059.00 to 10,000.00 Euros. The unique ID of the conversion record was "4c52215f-ca4b-4dcb-a7ae-36edc4f5db16". We want to settle that conversion now, so we add the conversion to the settlement using the **Add Conversion to Settlement** endpoint.

``POST /v2/settlements/a937f05e-e9fd-442e-a46f-11e84ba37806/add_conversion`` \
``Content-Type: multipart/form-data``

| Parameter Name    | Parameter Type | Example Value                            |
| ----------------- | -------------- | ---------------------------------------- |
| ``conversion_id`` | Payload        | ``4c52215f-ca4b-4dcb-a7ae-36edc4f5db16`` |
| ``X-Auth-Token``  | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2``     |

Example response:

```
{
    "id": "a937f05e-e9fd-442e-a46f-11e84ba37806",
    "short_reference": "20140101-BCDFGH",
    "status": "open",
    "conversion_ids": ["4c52215f-ca4b-4dcb-a7ae-36edc4f5db16"],
    "entries": {
        "GBP": {
            "send_amount": "8059.00",
            "receive_amount": "0.00"
        },
        "EUR":{
            "send_amount": "0.00",
            "receive_amount": "10000.00"
        }
    },
    "created_at": "2018-02-02T12:17:05+00:00",
    "updated_at": "2018-02-02T12:17:05+00:00",
    "released_at": "2018-02-02T12:17:05+00:000"
}
```

If you wish to settle multiple conversions in bulk, go ahead and make additional calls to the **Add Conversion to Settlement** endpoint, passing in different conversion IDs.


## Release Settlement
Finally, call the **Release Settlement** endpoint. This queues the conversions for processing. No further conversions can be added to a settlement while it is in a released status.


``POST /v2/settlements/a937f05e-e9fd-442e-a46f-11e84ba37806/release`` \
``Content-Type: multipart/form-data``

| Parameter Name    | Parameter Type | Example Value                            |
| ----------------- | -------------- | ---------------------------------------- |
| ``X-Auth-Token``  | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2``     |

Example response:

```
{
    "id": "a937f05e-e9fd-442e-a46f-11e84ba37806",
    "short_reference": "20140101-BCDFGH",
    "status": "released",
    "conversion_ids": ["4c52215f-ca4b-4dcb-a7ae-36edc4f5db16"],
    "entries": {
        "GBP": {
            "send_amount": "8059.00",
            "receive_amount": "0.00"
        },
        "EUR":{
            "send_amount": "0.00",
            "receive_amount": "10000.00"
        }
    },
    "created_at": "2018-02-02T12:17:05+00:00",
    "updated_at": "2018-02-02T12:18:15+00:00",
    "released_at": "2018-02-02T12:18:15+00:000"
}
```
