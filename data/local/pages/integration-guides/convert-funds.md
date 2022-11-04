[_metadata_:menu_title]:- "Converting funds from one currency to another"
[_metadata_:order]:- "8"

# Converting funds from one currency to another

A conversion is the process of trading money held in one currency for money in another currency.

## TL;DR
The steps and endpoints for making a conversion are:
1.  Get a detailed, tradable rate quote to convert money from one currency to another - [Get Detailed Rates](/api-reference/#get-detailed-rates).
2.  Create the conversion by calling the [Create Conversion](/api-reference/#create-conversion) endpoint.

A detailed worked example is provided in the integration guide below.

## Workflow diagrams

### For house accounts:
![rates and conversions](/images/workflow_diagrams/4_rates_and_conversions_house_account_level.jpg)

### For sub-accounts:
![rates and conversions](/images/workflow_diagrams/5_rates_and_conversions_on_behalf_of.jpg)


## Integration guide

In this guide, you will:

1.  Get a quote for trading Pound Sterling (GBP) for Euros (EUR).
2.  Top up your Euros balance by trading some Pound Sterling.

## Step 1: Login

Please refer to the [Authentication guide](/guides/integration-guides/authentication) for instructions for starting a new API session.

## Step 2: Get a quote

Check how much it will cost to buy 10,000 Euros using funds from your Pound Sterling balance, by making a call to the [Get Detailed Rates ](/api-reference/#get-detailed-rates)endpoint.

`GET /v2/rates/detailed`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Query String | `EUR` |
| `sell_currency` | Query String | `GBP` |
| `amount` | Query String | `10000.00` |
| `fixed_side` | Query String | `buy` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

On success, the response payload will contain details of Currencycloud's quotation to make the conversion. The following example tells you that you can sell £8,059 to buy €10,000. Please note, the quote is only indicative and a conversion must be booked to lock a rate.

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

## Step 3: Convert

If you're happy with the quote, you may create the conversion by calling the [Create Conversion ](/api-reference/#create-conversion) endpoint.

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

On success, the payload of the response message will contain full details of the conversion as recorded against your Currencycloud account.

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

This conversion will settle automatically on the `settlement_date` as long as there are sufficient funds in the account's GBP balance to cover the `client_sell_amount`. Please use your Cash Manager to top up your GBP balance if necessary.
