[_metadata_:menu_title]:- "Checking foreign exchange rates"
[_metadata_:order]:- "6"

# Checking foreign exchange rates

A foreign exchange (FX) rate is a rate at which one currency is exchanged for another. For example, an exchange rate of 114 Japanese Yen to the US Dollar means that ¥114 can be bought for US$1, or US$1 can be bought for ¥114.


## TL;DR
Currencycloud's API provides two endpoints for checking foreign exchange rates.
1.  Get indicative foreign exchange rate information for one or more currency pairs in a single request - [Get Basic Rates](/api-reference/#get-basic-rates).
2.  Get a detailed, tradable rate quote to convert money from one currency to another - [Get Detailed Rates](/api-reference/#get-detailed-rates). The quote provided is based on the [spread table](/guides/integration-guides/adding-an-fx-spread) of the authenticated user. There is also the option to provide a specific date for the conversion to occur.

Detailed instructions are given below.


## Integration guide

## Step 1: Login

Please refer to the [Authentication guide](/guides/integration-guides/authentication) for instructions for starting a new API session.

## Step 2: Get basic exchange rate information

Currencycloud's [Get Basic Rates endpoint](/api-reference/#get-basic-rates) provides real-time exchange rate data.

Quotes are given on currency pairs. A currency pair is two standard currency codes joined together: "EURUSD", "GBPUSD", "GBPJPY", etc. The first currency in the pair is the base currency. The second is the quote currency. The result indicates how much of the quote currency is needed to buy one unit of the base currency.

For example, to find out how many Pound Sterling (GBP) are needed to buy EUR €1.00, make the following HTTP call. Note the use of the currency pair "EURGBP" in the query string.

```
GET /v2/rates/find?currency_pair=EURGBP
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

If exchange rate information is available for the requested currency pair, you'll get a response similar to the following.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "rates": {
    "EURGBP": [
      "0.805300",
      "0.805900"
    ]
  },
  "unavailable": []
}

```

The two rates in the response are the "bid" and "offer" prices. The bid price is applicable if you are selling the base currency. The offer rate is applicable if you are buying the base currency. So, in the example above:

Selling EUR €1,000.00 would buy GBP £805.30.  
To buy EUR €1,000.00 you would need to sell GBP £805.90.

When you fetch exchange rate information from the [Get Basic Rates](/api-reference/#get-basic-rates) endpoint, the returned currency pair string will match the value of the currency_pair input parameter. 

## Step 3: Get a detailed quote

To find out *exactly* how much it will cost you to trade funds in one currency for another, use Currencycloud's [Get Detailed Rates](/api-reference/#get-detailed-rates) endpoint. For example, to get a quote buy 10,000 Euros using funds from your Pound Sterling balance, make the following call:

`GET /v2/rates/detailed`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `buy_currency` | Query String | `EUR` |
| `sell_currency` | Query String | `GBP` |
| `amount` | Query String | `10000.00` |
| `fixed_side` | Query String | `buy` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

On success, the response payload will contain details of Currencycloud's quotation to make the conversion. The following example tells you that you can sell GBP £8,059 to buy EUR €10,000. Please note, any quote is only ever indicative and a conversion must be booked to secure the rate.

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "settlement_cut_off_time": "2021-06-05T13:00:00Z",
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

When you fetch exchange rate information from the [Get Basic Rates](/api-reference/#get-basic-rates) endpoint, the returned currency pair string will match exactly the value of the `currency_pair` input parameter. However, when you get a quote from the [Get Detailed Rates](/api-reference/#get-detailed-rates) endpoint, the value of the `currency_pair` property in the response will be standardised, adhering to market conventions for currency pair notation.

It is conventional to represent a pairing of Euros to Pound Sterling as "EURGBP", never "GBPEUR", regardless which of the two currencies you are buying and selling. By default, the least valuable currency is the second unit in a currency pair. But there are some exceptions. If any of the following currencies are quoted against each other, then the currency appearing first in the list will be the first in the currency pair.

EUR  
GBP  
AUD  
NZD  
USD
