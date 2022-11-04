[_metadata_:menu_title]:- "Integration FAQ"
[_metadata_:order]:- "5"

# Integration FAQ

We have put together this document to answer questions that we are frequently asked by developers. If your question isn't answered here, please [get in touch](https://www.currencycloud.com/contact/).

## Convert

### When requesting a rate, is the ordering of the currencies significant?
Yes. When you fetch exchange rate information from the [Get Basic Rates](/api-reference/#get-basic-rates) endpoint, the returned currency pair string will match the value of the currency_pair input parameter.

When you get a quote from the [Get Detailed Rates](/api-reference/#get-detailed-rates) endpoint, however, the value of the currency_pair property in the response will be standardised, adhering to market conventions for currency pair notation which does not consider the buy/sell order.

See our [foreign exchange rates guide](/guides/integration-guides/check-foreign-exchange-rates/) for more information.

### How can I apply a mark-up to conversions?

The first step is to call the [Get Detailed Rates ](/api-reference/#get-detailed-rates)endpoint.

Amongst other response fields, this will give you the `client_rate`. Using your own mechanism, you can calculate an additional markup to the client rate and display this marked-up rate. You should also display the appropriate buy or sell amounts to your end customer for approval before executing the conversion request, this is also known as the "all-in price". This is either the `client_buy_amount` or `client_sell_amount`, depending on which is fixed.

For example, imagine you decide to apply a 0.5% mark-up on a trade to buy 1000 USD from a GBP balance. The call to [Get Detailed Rates](/api-reference/#get-detailed-rates) passes the parameters below:

| **Parameter Name** | **Parameter Type** | **Value** |
| --- | --- | --- |
| buy_currency | Query String | USD |
| sell_currency | Query String | GBP |
| amount | Query String | 1000.00 |
| fixed_side | Query String | buy |
| on_behalf_of | Query String | 1b0d6b8d-1d61-445d-8cda-a73e4c24265c |
| X-Auth-Token | Header | ea6d13c7bc50feb46cf978d137bc01a2 |

Note that the fixed side is set to 'buy'.

A successful response payload will look like this:

```
{
    "settlement_cut_off_time": "2021-10-05T15:30:00Z",
    "currency_pair": "GBPUSD",
    "client_buy_currency": "USD",
    "client_sell_currency": "GBP",
    "client_buy_amount": "1000.00",
    "client_sell_amount": "710.28",
    "fixed_side": "buy",
    "client_rate": "1.4079",
    "partner_rate": "1.4079",
    "core_rate": "1.4079",
    "deposit_required": false,
    "deposit_amount": "0.0",
    "deposit_currency": "GBP",
    "mid_market_rate": "1.4080"
}
```

Taking the `partner_rate` of 1.4079, you would apply a mark-up of 0.5% to it -- in this case this means subtracting 0.5% from the rate to show the customer a rate of 1.4009 (= 1.4079 x (1 -- 0.005)). If you were selling USD to GBP, you would instead add 0.5% to the rate.

Since the buy-side was fixed, the  `client_sell_amount` should also be adjusted and displayed to your customer for approval,  it will also be part of the final conversion request. In our example, the adjusted `client_sell_amount`would be:  

£710.28 x 0.005 (markup) = £3.55

£3.55 + £710.28= **£713.84** (final `client_sell_amount`).

When you book the conversion, you would pass in the final `client_sell_amount`.

### How should I handle FX quotations as Currencycloud always shows live rates?

Since the rates that we provide are real time rates, we advise that you build in a timer or count-down to your application so that customers can confirm the displayed rate (live/indicative) within a specified time limit. This helps to mitigate your forex risk.

In addition, you may choose to provide a marked up rate to the customer, please see the previous question for details on how to achieve this.  Adding a markup to the rates allows you to gain profit on trades and also helps mitigate your forex risk.

### How should I use the unique_request_id parameters?

The `unique_request_id` is available as a parameter on the [Create Conversion](/api-reference/#conversions), [Create Payment](/api-reference/#payments) and [Create Transfer](/api-reference/#create-transfer) APIs in order to allow you to give a transaction a unique identifier.  The purpose is two-fold: to help with the identification of a transaction, making searching easier; and as an idempotency key -- this ensures that if you send duplicate requests to us we will not create multiple records.

## Pay

### Can I validate a beneficiary's account details?

Yes, the[ Validate Beneficiary](/api-reference/#validate-beneficiary) endpoint will provide feedback on whether the data entered matches the requirements to create the beneficiary. We verify the beneficiary details when creating a payment.

### What is the default SWIFT charge type?

The initial default applied to an account is SWIFT Shared. The default can be configured to be either Shared (SHA) or Ours (OUR) depending on your specific needs. When making a payment, if no payment charge type is selected, then the default charge type of the account applies to the payment.

More information can be found in our [Help Center.](https://support.currencycloud.com/hc/en-gb/articles/360017430820)

### How do I manage Purpose of Payment information?

Use our  [ Get Payment Purpose Code](/api-reference/#get-payment-purpose-codes) endpoint to get a list of payment purpose codes for the currency and entity type (company or individual). Please note that the `entity_type` in the response refers to the payer entity type, not the recipient.

When [Creating a Payment, ](/api-reference/#create-payment)place the purpose of payment code in the `purpose_code` parameter.

Purpose of Payment information is only applicable to certain payment routes/currencies/scenarios, please do not pass a purpose code if it is not required as the API request will be rejected.

More information on these scenarios and the valid purpose codes can be found in our [Help Center](https://support.currencycloud.com/hc/en-gb/articles/360017430000-Payment-Purpose-Codes).

### What is the mapping of parameters from the Get Beneficiary Requirements endpoint to Create Beneficiary?

There is no one to one mapping. Some data translation needs to be made from the response from [Get Beneficiary Requirements](/api-reference/#get-beneficiary-requirements) to [Create Beneficiary](/api-reference/#create-beneficiary) (for example, acct_number >> account_number).

## Manage

### Do you have an endpoint for opening specific currency wallets?

Yes, call our [Get Balance](/api-reference/#get-balance) endpoint for the chosen currency. If no wallet exists for this currency then one will be created.

Alternatively, a wallet will be opened upon a receipt or a conversion to the currency.
