# Convert Money
Buy more Euros using funds from your Pound Sterling balance.


## First Steps

1. [Authenticate](authenticate.md)
2. [Check your currency balances](check-balance.md)


## Get a Quote
Check how much it will cost to buy 10,000 Euros using funds from your Pound Sterling balance, by making a call to the **Get Detailed Rates** endpoint.

``GET /v2/rates/detailed``

| Parameter Name    | Parameter Type | Example Value                        |
| ----------------- | -------------- | ------------------------------------ |
| ``buy_currency``  | URI Query      | ``EUR``                              |
| ``sell_currency`` | URI Query      | ``GBP``                              |
| ``amount``        | URI Query      | ``10000.00``                         |
| ``fixed_side``    | URI Query      | ``buy``                              |
| ``X-Auth-Token``  | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

On success, the response payload will contain details of Currencycloud's quotation to make the conversion. This information tells you that you can sell GBP 8,059 to buy 10,000 Euros. The quote is valid until 2pm on 6 February 2018 (UTC time).

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "settlement_cut_off_time": "2018-02-06T14:00:00Z",
    "currency_pair": "EURGBP",
    "client_buy_currency": "EUR",
    "client_sell_currency": "GBP",
    "client_buy_amount": "10000.00",
    "client_sell_amount": "8059.00",
    "fixed_side": "buy",
    "client_rate": "0.8059",
    "partner_rate": null,
    "core_rate": "0.8059",
    "deposit_required": false,
    "deposit_amount": "0.0",
    "deposit_currency": "GBP",
    "mid_market_rate": "0.8056"
}
```


## Convert
If you are happy with the quote, you may authorize the conversion by calling the **Create Conversion** endpoint.

``POST /v2/conversions/create`` \
``Content-Type: multipart/form-data``

| Parameter Name     | Parameter Type | Example Value                        |
| ------------------ | -------------- | ------------------------------------ |
| ``buy_currency``   | Payload        | ``EUR``                              |
| ``sell_currency``  | Payload        | ``GBP``                              |
| ``amount``         | Payload        | ``10000.00``                         |
| ``fixed_side``     | Payload        | ``buy``                              |
| ``reason``         | Payload        | ``EUR topup``                        |
| ``term_agreement`` | Payload        | ``true``                             |
| ``X-Auth-Token``   | Header         | ``ea6d13c7bc50feb46cf978d137bc01a2`` |

On success, the payload of the response message will contain full details of the conversion as recorded against your Currencycloud account. Note, this does not mean that the conversion has taken place. For that to happen, you will need to [add the conversion to a settlement](settle.md), and have enough funds in your GBP balance on the settlement date. Conversions will be processed asynchronously, and the additional funds will be available in the purchase currency after the settlement date.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": "4c52215f-ca4b-4dcb-a7ae-36edc4f5db16",
    "settlement_date": "2018-02-06T14:00:00+00:00",
    "conversion_date": "2018-02-06T00:00:00+00:00",
    "short_reference": "20180202-FYYXFH",
    "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
    "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
    "currency_pair": "EURGBP",
    "status": "awaiting_funds",
    "buy_currency": "EUR",
    "sell_currency": "GBP",
    "client_buy_amount": "10000.00",
    "client_sell_amount": "8059.00",
    "fixed_side": "buy",
    "core_rate": "0.8059",
    "partner_rate": "",
    "partner_status": "funds_arrived",
    "partner_buy_amount": "0.00",
    "partner_sell_amount": "0.00",
    "client_rate": "0.8059",
    "deposit_required": false,
    "deposit_amount": "0.00",
    "deposit_currency": "",
    "deposit_status": "not_required",
    "deposit_required_at": "",
    "payment_ids": [],
    "unallocated_funds": "0.00",
    "unique_request_id": null,
    "created_at": "2018-02-02T11:41:29+00:00",
    "updated_at": "2018-02-02T11:41:29+00:00",
    "mid_market_rate": "0.8056"
}
```


## Next Steps

[Make a payment to Germany from your Euros balance](pay.md). And remember, before conversions can be processed, you must [create a settlement](settle.md).
