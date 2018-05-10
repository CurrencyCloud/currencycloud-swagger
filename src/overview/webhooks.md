# Webhooks  
To get notifications about the status of your payments and conversions, you can setup webhooks. These are endpoints on your servers that Currencycloud will push data to via an HTTP ``POST`` request when we have something to tell you.

Webhooks are a powerful tool. They are the mechanism by which you can automate the tracking of your transactions. You can use webhooks to listen for the following events:

- New payment
- Payment release
- Payment failure
- Conversion waiting funds
- Conversion funds arrived
- Conversion trade settled
- Conversion trade closed
- Trade execution

Notifications are posted with the following JSON payload.

```
{
  "header": {
    "notification_type": "trade_notification",
    "message_type": "conversion"
  },
  "body": {
    "id": "cdbb5166-81ef-48d3-bcba-b22bd7e45ca1",
    "settlement_date": "2015-12-11T14:00:00+00:00",
    "conversion_date": "2015-12-11T00:00:00+00:00",
    "short_reference": "20151209-NMRTMN",
    "creator_contact_id": "bed9cdd1-05b4-0132-bcdc-002219414986",
    "account_id": "bec9a130-05b4-0132-bcdb-002219414986",
    "currency_pair": "EURGBP",
    "status": "awaiting_funds",
    "buy_currency": "GBP",
    "sell_currency": "EUR",
    "client_buy_amount": "726.59",
    "client_sell_amount": "999.99",
    "fixed_side": "sell",
    "mid_market_rate": "0.7269",
    "core_rate": "0.7266",
    "partner_rate": "",
    "partner_status": "funds_arrived",
    "partner_buy_amount": "0.00",
    "partner_sell_amount": "0.00",
    "client_rate": "0.7266",
    "deposit_required": false,
    "deposit_amount": "0.00",
    "deposit_currency": "",
    "deposit_status": "not_required",
    "deposit_required_at": "",
    "payment_ids": [ "bc021f0a-9794-431f-a8ef-e18f2eafdb59" ],
    "created_at": "2015-12-09T03:07:13+00:00",
    "updated_at": "2015-12-09T03:07:14+00:00"
  }
}
```

The ``header`` object contains meta data about the payload including the message type and the notification type. There are only three possible combinations of values in this section:

| notification_type              | message_type  |
| ------------------------------ | ------------- |
| payment_released_notification  | payment       |
| payment_failed_notification    | payment       |
| trade_notification             | conversion    |

Although the webhooks are your own, hosted on your own servers, we have strict requirements about the endpoints that we can transmit financial information to. For example, we require your webhook service to be secured by one of preferred Certificate Authorities. Before you get started coding your webhook endpoints, we recommend that you first [contact our support team](../support.md) to discuss the requirements.
