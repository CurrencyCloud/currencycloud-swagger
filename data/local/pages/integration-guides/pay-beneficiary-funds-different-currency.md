[_metadata_:menu_title]:- "Paying a beneficiary using funds in a different currency"
[_metadata_:order]:- "8"

# Paying a beneficiary using funds in a different currency

This guide explains how you can make a payment in a different currency and also how to ensure that you have enough balance available to make the payment.

## TL;DR

The steps and endpoints for making a payment in a chosen currency are:

1. Check the balance for the payment currency by calling [Get Balance](/api-reference/#balances), passing the currency as a parameter. Alternatively, get the balances for all currencies you hold by calling [Find Balances](/api-reference/#find-balances).
2. If you don't have enough balance to cover the payment, you can convert funds - first call [Get Detailed Rates](/api-reference/#get-detailed-rates) to get a rate, you can then go ahead and convert funds by calling  [Create Conversion](/api-reference/#create-conversion).
3. Find out what details you need to provide to make a payment to the beneficiary by calling [Get Beneficiary Requirements](/api-reference/#get-beneficiary-requirements), passing the currency and country as parameters.
4.	Find an existing beneficiary or create a new one - [Find Beneficiaries](/api-reference/#find-beneficiaries) /
[Create Beneficiary](/api-reference/#create-beneficiary).
5.	Find out what payer details are required for the payment - [Get Payer Requirements](/api-reference/#get-payer-requirements).
6.	Create the payment - [Create Payment](/api-reference/#create-payment).

Detailed instructions are given below.


## Integration guide

In this guide, we will:

1. Check how much money you hold in various foreign currencies in your Currencycloud account.  
2. Top up your Euros balance by trading some Pound Sterling.  
3. Make a payment in Euros to a beneficiary in Germany.
Note, this functionality is available only via the live API, not the demo API.

## Step 1: Login

Please refer to the [authentication guide](/guides/integration-guides/authentication) for instructions for starting a new API session.

## Step 2: Check available balances

To find out how many Euros you have, call the [Get Balance](/api-reference/#get-balance) endpoint, passing `EUR` as the third URI path parameter.

`GET /v2/balances/EUR`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

The following response shows that you hold €15,458.12 in your main Currencycloud account.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
  "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
  "currency": "EUR",
  "amount": "15458.12",
  "created_at": "2021-12-10T16:05:20+00:00",
  "updated_at": "2021-12-10T16:05:20+00:00"
}

```

Alternatively, you can check the balances for all foreign currencies that you hold in your Currencycloud account by calling the [Find Balances](/api-reference/#find-balances) endpoint.

`GET /v2/balances/find`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

The following response shows that you hold £10,750.00, US$1,500.24 and €15,458.12 in your main Currencycloud account.

```
{
  "balances": [
    {
      "id": "c52128a4-3918-40dc-a92a-7225cef3a4a6",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "GBP",
      "amount": "10750.00",
      "created_at": "2021-12-10T16:05:19+00:00",
      "updated_at": "2021-12-10T16:05:19+00:00"
    },
    {
      "id": "349a2b87-9455-4808-9e68-515daf1f7298",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "USD",
      "amount": "1550.24",
      "created_at": "2021-12-10T16:05:19+00:00",
      "updated_at": "2021-12-10T16:05:19+00:00"
    },
    {
      "id": "ad6411db-1e00-44fd-b4e8-194c74cf2f83",
      "account_id": "d22073a6-4c56-4980-8699-504b0c70003f",
      "currency": "EUR",
      "amount": "15458.12",
      "created_at": "2021-12-10T16:05:20+00:00",
      "updated_at": "2021-12-10T16:05:20+00:00"
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

In this instance, you do not have sufficient EUR available to make the 10,000 EUR payment to Germany. You can either send us additional EUR or convert funds from the available GBP balance.

## Step 3: Top up

Check how much it will cost to buy 10,000 Euros using funds from your Pound Sterling balance, by making a call to the [Get Detailed Rates](/api-reference/#get-detailed-rates) endpoint.

`GET /v2/rates/detailed`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Query String | `EUR` |
| `sell_currency` | Query String | `GBP` |
| `amount` | Query String | `10000.00` |
| `fixed_side` | Query String | `buy` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

On success, the response payload will contain details of Currencycloud's quotation to make the conversion. The following example tells you that you can sell £8,059 to buy $10,000. The quote is valid until 2pm on 6 February 2021 (UTC time).

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "settlement_cut_off_time": "2021-02-06T14:00:00Z",
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

If you're happy with the quote, you may authorize the conversion by calling the [Create Conversion](/api-reference/#create-conversion) endpoint.

`POST /v2/conversions/create`\
`Content-Type: multipart/form-data`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Form Data | `EUR` |
| `sell_currency` | Form Data | `GBP` |
| `amount` | Form Data | `10000.00` |
| `fixed_side` | Form Data | `buy` |
| `reason` | Form Data | `Top up Euros balance` |
| `term_agreement` | Form Data | `true` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

On success, the payload of the response message will contain full details of the conversion as recorded against your Currencycloud account. Make a note of the unique conversion id (the `id` field), you'll need this if you want to link the conversion and payment. This means that the payment won’t be processed until the conversion settles. If you cancel the conversion, the payment itself will move to a status of `suspended`, you would have to re-create the payment again for the status to move to `ready_to_send`.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "4c52215f-ca4b-4dcb-a7ae-36edc4f5db16",
  "settlement_date": "2021-02-06T14:00:00+00:00",
  "conversion_date": "2021-02-06T00:00:00+00:00",
  "short_reference": "20210202-FYYXFH",
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
  "created_at": "2021-02-02T11:41:29+00:00",
  "updated_at": "2021-02-02T11:41:29+00:00",
  "mid_market_rate": "0.8056"
}

```

Notice the `status` field in conversion object, above. A conversion has five possible states:

- Awaiting funds (`awaiting_funds`)

- Funds sent (`funds_sent`)  

- Funds arrived (`funds_arrived`)

- Trade settled (`trade_settled`)

- Closed (`closed`)

This conversion is currently awaiting funds.

## Step 4: Check payment requirements

Check what details are required to make a regular (local) payment in Euros to a beneficiary with a bank account in Germany. To do that, call the [Get Beneficiary Requirements](/api-reference/#get-beneficiary-requirements) endpoint.

`GET /v2/reference/beneficiary_required_details`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `currency` | Query String | `EUR` |
| `bank_account_country` | Query String | `DE` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

The following response tells us that, to make a regular payment to a German bank account in Euros, we need two pieces of information: the IBAN and BIC/SWIFT numbers for the beneficiary. The beneficiary could be either a company or an individual. Either way, the same information is required.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "details": [
    {
      "payment_type": "priority",
      "beneficiary_entity_type": "individual",
      "beneficiary_address": "^.{1,255}",
      "beneficiary_city": "^.{1,255}",
      "beneficiary_country": "^[A-z]{2}$",
      "beneficiary_first_name": "^.{1,255}",
      "beneficiary_last_name": "^.{1,255}",
      "iban": "([A-Z0-9]\\s*){15,34}",
      "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$"
    },
    {
      "payment_type": "priority",
      "beneficiary_entity_type": "company",
      "beneficiary_address": "^.{1,255}",
      "beneficiary_city": "^.{1,255}",
      "beneficiary_country": "^[A-z]{2}$",
      "beneficiary_company_name": "^.{1,255}",
      "iban": "([A-Z0-9]\\s*){15,34}",
      "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$"
    },
    {
      "payment_type": "regular",
      "iban": "([A-Z0-9]\\s*){15,34}",
      "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$",
      "beneficiary_entity_type": "individual"
    },
    {
      "payment_type": "regular",
      "iban": "([A-Z0-9]\\s*){15,34}",
      "bic_swift": "^[0-9A-Z]{8}$|^[0-9A-Z]{11}$",
      "beneficiary_entity_type": "company"
    }
  ]
}

```

## Step 5: Add a beneficiary

If you know the required details, you can go ahead and create a record for the beneficiary via the [Create Beneficiary](/api-reference/#create-beneficiary) endpoint.

`POST /v2/beneficiaries/create`\
`Content-Type: multipart/form-data`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `name` | Form Data | `Acme GmbH` |
| `bank_account_holder_name` | Form Data | `Acme GmbH` |
| `currency` | Form Data | `EUR` |
| `beneficiary_country` | Form Data | `DE` |
| `bank_country` | Form Data | `DE` |
| `bic_swift` | Form Data | `COBADEFF` |
| `iban` | Form Data | `DE89370400440532013000` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

If the beneficiary is successfully created, the response message will contain full details about the beneficiary as recorded in your Currencycloud account. Note the beneficiary's unique ID (`id`). You'll need this to make a payment to the beneficiary, in the next step.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
  "bank_account_holder_name": "Acme GmbH",
  "name": "Acme GmbH",
  "email": null,
  "payment_types": [
    "regular"
  ],
  "beneficiary_address": [],
  "beneficiary_country": "DE",
  "beneficiary_entity_type": null,
  "beneficiary_company_name": null,
  "beneficiary_first_name": null,
  "beneficiary_last_name": null,
  "beneficiary_city": null,
  "beneficiary_postcode": null,
  "beneficiary_state_or_province": null,
  "beneficiary_date_of_birth": null,
  "beneficiary_identification_type": null,
  "beneficiary_identification_value": null,
  "bank_country": "DE",
  "bank_name": "Test Bank Plc",
  "bank_account_type": null,
  "currency": "EUR",
  "account_number": null,
  "routing_code_type_1": null,
  "routing_code_value_1": null,
  "routing_code_type_2": null,
  "routing_code_value_2": null,
  "bic_swift": "COBADEFF",
  "iban": "DE89370400440532013000",
  "default_beneficiary": "false",
  "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
  "bank_address": [],
  "created_at": "2021-02-02T11:52:23+00:00",
  "updated_at": "2021-02-02T11:52:23+00:00",
  "beneficiary_external_reference": null
}

```

## Step 6: Make a payment

Authorize a payment by calling the [Create Payment](/api-reference/#create-payment) endpoint. Optionally, you may provide an idempotency key (via the `unique_request_id` parameter). This helps protect against accidental duplicate payments.

`POST /v2/payments/create`\
`Content-Type: multipart/form-data`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `currency` | Form Data | `EUR` |
| `beneficiary_id` | Form Data | `aea097c2-39e4-49b5-aaa6-c860ca55ca0b` |
| `amount` | Form Data | `10000` |
| `reason` | Form Data | `Invoice Payment` |
| `payment_type` | Form Data | `regular` |
| `reference` | Form Data | `2021-014` |
| `unique_request_id` | Form Data | `4abd730f-bb50-4b4a-8890-f46addff222b` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

You can link the payment to the conversion by passing the `conversion_id` as a parameter. Under these circumstances, the payment won’t be processed/actioned until the conversion settles. If you cancel the conversion, the payment itself will move to a status of "suspended" and you would have to re-create the payment again for the status to move to "ready_to_send”.

If the payment is successfully queued, the response payload will contain all the information about the payment as recorded in your Currencycloud account. This does not mean that the payment was made. It just means that it is ready for processing.

Payments are processed asynchronously. Currencycloud will process payments on the `payment_date` specified, provided you hold enough money in the relevant currency at the time. It is possible to instruct payments even if you don't hold enough money in the relevant currency. The payments will be queued in the normal way but will not be processed until your account balance is topped up.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "bea05ec4-8c6b-4ec9-80e5-65c0cd257473",
  "amount": "10000.00",
  "beneficiary_id": "aea097c2-39e4-49b5-aaa6-c860ca55ca0b",
  "currency": "EUR",
  "reference": "2021-014",
  "reason": "Invoice Payment",
  "status": "ready_to_send",
  "creator_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
  "payment_type": "regular",
  "payment_date": "2021-02-02",
  "transferred_at": "",
  "authorisation_steps_required": "0",
  "last_updater_contact_id": "1993263d-be07-42d4-b75b-ae4ea18bcb6c",
  "short_reference": "180202-RDRWGQ001",
  "conversion_id": null,
  "failure_reason": "",
  "payer_id": "49d44eff-af91-45b0-a32e-84c7c1750ca0",
  "payer_details_source": "account",
  "created_at": "2021-02-02T11:56:05+00:00",
  "updated_at": "2021-02-02T11:56:05+00:00",
  "payment_group_id": null,
  "unique_request_id": "4abd730f-bb50-4b4a-8890-f46addff222b",
  "failure_returned_amount": "0.00",
  "ultimate_beneficiary_name": null
}
```
