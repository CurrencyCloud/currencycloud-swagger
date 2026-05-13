[_metadata_:menu_title]:- "Adding an FX Spread"
[_metadata_:order]:- "11"

# Adding an FX Spread/Markup

If you are looking to apply static markup, please use spread tables and contact your Account Manager or our support team at <a href="mailto:support@currencycloud.com">support@currencycloud.com</a>. This guide walks through how to **manually** set the markup on a trade.

Adding a markup enables you to earn a profit on a forex trade. The calculated markup is passed in the conversion request to lock in the desired rate. Please note that markup is only supported when executing conversions on behalf of a sub-account (also known as a named account). Please refer to our [sub-account activity guide](https://developer.currencycloud.com/guides/integration-guides/sub-account-activity) for more information on how to conduct activity at the sub-account level.

Any profit earned on conversions is generated at the sub-account level and aggregated to your house account. These profits are reconciled and paid out as a monthly commission.

## Step 1: Login

Please refer to the [authentication guide](https://developer.currencycloud.com/guides/integration-guides/authentication) for instructions for establishing a new API session.

## Step 2: Get a quote

As an example, let's check how much it will cost to buy 10,000 EUR using funds from your customer's GBP balance, by making a call to the [Get Detailed Rates](https://developer.currencycloud.com/api-reference/#get-detailed-rates) endpoint.

Example request 1:

`GET /v2/rates/detailed`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Query String | `EUR` |
| `sell_currency` | Query String | `GBP` |
| `amount` | Query String | `10000.00` |
| `fixed_side` | Query String | `buy` |
| `on_behalf_of` | Query String | `1b0d6b8d-1d61-445d-8cda-a73e4c24265c` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

Example response 1:

```
HTTP/1.1 200 OK

Content-Type: application/json

{
  "settlement_cut_off_time": "2021-07-15T13:30:00Z",
  "currency_pair": "EURGBP",
  "client_buy_currency": "EUR",
  "client_sell_currency": "GBP",
  "client_buy_amount": "10000.00",
  "client_sell_amount": "8057.00",
  "fixed_side": "buy",
  "client_rate": "0.8057",
  "partner_rate": "0.8057",
  "core_rate": "0.8057",
  "deposit_required": false,
  "deposit_amount": "0.0",
  "deposit_currency": "GBP",
  "mid_market_rate": "0.8056"
}
```

Example request 2:

`GET /v2/rates/detailed`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Query String | `GBP` |
| `sell_currency` | Query String | `EUR` |
| `amount` | Query String | `10000.00` |
| `fixed_side` | Query String | `sell` |
| `on_behalf_of` | Query String | `1b0d6b8d-1d61-445d-8cda-a73e4c24265c` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

Example response 2:

```
HTTP/1.1 200 OK

Content-Type: application/json

{
  "settlement_cut_off_time": "2021-07-15T13:30:00Z",
  "currency_pair": "EURGBP",
  "client_buy_currency": "GBP",
  "client_sell_currency": "EUR",
  "client_buy_amount": "8057.00",
  "client_sell_amount": "10000.00",
  "fixed_side": "sell",
  "client_rate": "0.8057",
  "partner_rate": "0.8057",
  "core_rate": "0.8057",
  "deposit_required": false,
  "deposit_amount": "0.0",
  "deposit_currency": "EUR",
  "mid_market_rate": "0.8056"
}
```
On success, the response payload will contain details of Currencycloud’s quotation to make the conversion. The responses above shows two cases

1	Request/Response 1 - your customer can sell £8,057 to buy €10,000.
2	Request/Response 2 - your customer can sell €10,000 to buy £8,057.

Please note, the quote is only indicative and a conversion must be booked to lock a rate.


## Step 3: Calculate the markup within your application

If you are specifying the `client_buy_amount`, it must not be more than the amount you buy on the market, and conversely, if you are specifying the `client_sell_amount`, it must not be less than the amount you sell on the market.

Using your own internal mechanism, you can calculate and add a markup to the `client_rate` from the response payload in step 2. You can then display this marked-up rate including the appropriate buy/sell amounts, also known as  the "all in price" (`client_buy_amount` or `client_sell_amount`, depending on which side is fixed) to your end customer for final approval before executing the conversion request. 

The base currency is the first currency in the `currency_pair`, while the quote currency is the second currency in the pair.

-	If the sell currency matches the quote currency in the `currency_pair`, the markup is **added** to the `partner_rate`.
-	If the sell currency matches the base currency in the `currency_pair`, the markup is **subtracted** from the `partner_rate`.

In the above example, the `currency_pair` is EURGBP and the `client_sell_currency` is GBP, so the markup is **added**.

For our example, let’s say you want to markup the client_rate by 0.5%.

### Calculating the client rate

1a. Formula 1a (when selling the quote currency — add markup):

  `client_rate = partner_rate + (markup × partner_rate)` <br><br>

Example: 0.8057 + (0.005 × 0.8057) = 0.8097

1b. Formula 1b (when selling the base currency — subtract markup):

  `client_rate = partner_rate - (markup × partner_rate)`  <br><br>

Example: 0.8057 - (0.005 × 0.8057) = 0.8017

Since the `buy-side` of the rate request was fixed in step 2 (by setting the `fixed_side` to “buy”), we need to reflect the markup in the `client_sell_amount` parameter. This should be displayed to your customer within your UI for approval and included in the conversion request as detailed in step 4.

We calculate the floating amount using the marked-up rate as follows:

### Calculating the client amount

2a. (`fixed_side` = “buy”, `client_sell_currency` = quote currency):

  `client_sell_amount = client_rate × client_buy_amount` <br><br>

Example:

- partner amount = 0.8057 × 10000 = 8057
- client amount = 0.8097 × 10000 = 8097

2b. (`fixed_side` = “buy”, `client_sell_currency` = base currency):

  `client_sell_amount = client_buy_amount / client_rate` <br><br>

Example:

- partner amount = 10000 / 0.8057 = 12411.57
- client amount = 10000 / 0.8017 = 12473.48

**The client amount must be greater or equal to the partner amount when the fixed side is buy.** <br> <br>

2c. (`fixed_side` = “sell”, `client_sell_currency` = quote currency):

  `client_buy_amount = client_sell_amount / client_rate` <br><br>

Example:

- partner amount = 8097 / 0.8057 = 10049.65
- client amount 8097 / 0.8097 = 10000.00

2d. (`fixed_side` = “sell”, `client_sell_currency` = base currency):

  `client_buy_amount = client_sell_amount × client_rate` <br><br>

Example:

- partner amount = 10000 × 0.8057 = 8057.00
- client amount = 10000 × 0.8017 = 8017.00

**The client amount must be less or equal to the core amount/partner amount when the fixed side is sell.**  <br><br>

If setting the fixed_side to “buy”, you must adjust and include the `client_sell_amount` in your conversion request. If the fixed_side is “sell”, you must adjust and include the `client_buy_amount` in your conversion request.

## Step 4: Submit the conversion

Once your customer is happy with the quote, you can create the conversion by calling the [Create Conversion](https://developer.currencycloud.com/api-reference/#create-conversion) endpoint, factoring in the calculated FX markup from step 3 by passing in and fixing the `client_sell_amount` or `client_buy_amount` parameter, depending on the fixed side. Passing in the value, rather than the marked-up rate, allows you to honor the amounts with your customers, while managing the risk of rate fluctuation.

This conversion will settle automatically on the `settlement_date` as long as there are sufficient funds in the account’s sell currency balance to cover the `client_sell_amount`. Please use your Cash Manager to top up your balance if necessary.

```
POST /v2/conversions/create
Content-Type: multipart/form-data
```


| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Form Data | `EUR` |
| `sell_currency` | Form Data | `GBP` |
| `amount` | Form Data | `10000.00` |
| `fixed_side` | Form Data | `buy` |
| `reason` | Form Data | `Top up Euros balance` |
| `term_agreement` | Form Data | `true` |
| `client_sell_amount` | Form Data | `8097` |
| `on_behalf_of` | Form Data | `1b0d6b8d-1d61-445d-8cda-a73e4c24265c` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

On success, the payload of the response message will contain full details of the conversion as recorded against your customer's Currencycloud account.

```
HTTP/1.1 200 OK

Content-Type: application/json

{
    "id": "1da6ecc1-88e2-4419-9383-477540847a6a",
    "settlement_date": "2021-07-15T13:30:00+00:00",
    "conversion_date": "2021-07-15T00:00:00+00:00",
    "short_reference": "20210713-VRRVYL",
    "creator_contact_id": "323ab1a3-84df-4c2f-a46a-8af62b08c72e",
    "account_id": "fd178af6-cc06-4088-97fb-e079ebf5c71c",
    "currency_pair": "EURGBP",
    "status": "awaiting_funds",
    "buy_currency": "EUR",
    "sell_currency": "GBP",
    "client_buy_amount": "10000.00",
    "client_sell_amount": "8097",
    "fixed_side": "buy",
    "core_rate": "0.8057",
    "partner_rate": "0.8057",
    "partner_buy_amount": "10000.00",
    "partner_sell_amount": "8057.00",
    "client_rate": "0.8097",
    "deposit_required": false,
    "deposit_amount": "0.00",
    "deposit_currency": "",
    "deposit_status": "not_required",
    "deposit_required_at": "",
    "payment_ids": [],
    "unallocated_funds": "10000.00",
    "unique_request_id": null,
    "created_at": "2021-07-13T10:25:15+00:00",
    "updated_at": "2021-07-13T10:25:16+00:00",
    "mid_market_rate": "0.8056"
}
```

Inspecting the `partner_buy_amount` and `partner_sell_amount` parameters shows that you are selling £8,057 to buy €10,000, this is the cost of the trade without markup.

The `client_buy_amount` and `client_sell_amount` parameters give the customer's costs for the trade, factoring in the 0.5% markup. The customer is selling £8097 to buy €10,000.

Your profit on this trade is the difference between the `client_sell_amount `and `partner_sell_amount` parameters; you will therefore make a profit of £40 on this trade.

### Example calculations with possible combinations

| Request Buy | Request Sell | Fixed Side | Amount | Floating Amount | Core Rate | Core Sell Amount | Core Buy Amount | Markup % | Client Rate | Client Amount | Client Amount Type |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EUR | GBP | buy | 10000 | 8057.00 | 0.8057 | 8057.00 | 10000.00 | 0.50% | 0.8097285 | 8097.29 | sell |
| EUR | GBP | sell | 10000 | 12411.57 | 0.8057 | 10000.00 | 12411.57 | 0.50% | 0.8097285 | 12349.82 | buy |
| GBP | EUR | buy | 10000 | 12411.57 | 0.8057 | 12411.57 | 10000.00 | 0.50% | 0.8016715 | 12473.94 | sell |
| GBP | EUR | sell | 10000 | 8057.00 | 0.8057 | 10000.00 | 8057.00 | 0.50% | 0.8016715 | 8016.72 | buy |
