[_metadata_:menu_title]:- "Push Notifications / Webhooks"
[_metadata_:order]:- "3"

# Push Notifications

## Overview

Push Notifications, or webhooks, allow you to set up integrations that correspond with 'notifications' from Currencycloud.

There is a set of events described in the Notifications section below that can trigger push notifications on the Currencycloud platform. When one of these events is triggered, we send an HTTP POST command to the webhook's URL. This allows you to track transactions and state changes in a more efficient manner and automate communications internally or with your customers.

## Security

We want you to be confident that the notifications come from Currencycloud and that they have not been tampered with. We therefore append a Hash-based Message Authentication Code (HMAC) to notifications to enable you to verify the integrity of the messages.  Find out how in our [Message Verification FAQ](https://support.currencycloud.com/hc/en-gb/articles/360018656600-Push-Notifications-Message-Verification-HMAC-FAQ).

## Versioning

In July 2021, we introduced versioning - this allows us to deliver changes to you quicker, without risking breaking your integration. By default, you will be delivered the most recent version of a notification type. We will notify you if and when we decide to deprecate a version and provide you with guidance on how to upgrade your integration. If you have any questions on this, please contact your Solutions Manager. 

## Automatic re-send functionality

In July 2021, we also introduced automatic re-send functionality. If a delivery fails the first time, we will automatically attempt to send it 5 more times, with an exponentially growing timeout between attempts, as per the list below:

1 second\
2 seconds\
4 seconds\
8 seconds\
16 seconds

After 5 attempts, the delivery will be marked as Failed. At this point, it is worth checking your configuration before asking your Solutions Manager to manually re-send the notification. 

## Message headers

Please note that we may at times send additional headers in our notifications.

## Getting started

When you are ready to get set up with push notifications, [please contact your Solutions Manager](https://www.currencycloud.com/contact/technical-support/). You will need to provide them with an endpoint which can be configured against our Demo and Production environments.

## Notifications and events

The following entities and events generate push notifications on the Currencycloud platform. These events can be configured individually to generate a push notification.

### Payments

The following diagram presents the different status payments go through during their lifecycle on the platform. This also highlights which statuses trigger push notifications.

![Payments](/images/push_notifications/pn_payments_diagram.png)

### Conversions

The following diagram presents the different statuses that a conversion goes through during its lifecycle on the platform. The diagram describes also which statuses trigger events that are covered by push notifications.

![Conversions](/images/push_notifications/pn_conversions_diagram.png)

### Transfers

The following diagram presents the different statuses that a transfer goes through during its lifecycle on the platform. The diagram describes also which statuses trigger events that are covered by push notifications.

![Transfers](/images/push_notifications/pn_transfers_diagram.png)

### Funding Transactions

The following diagram presents the details of a funding transaction.

![Funding](/images/push_notifications/pn_funding_transactions_diagram.png)


### Onboarding

The diagram below shows the possible status of an onboarding form along with status trigger events that are covered by push notifications.

![Onboarding](/images/push_notifications/pn_onboarding_diagram.png)


### Bank Account Verification

[Bank Account Verification ](https://support.currencycloud.com/hc/en-gb/articles/360018656080-Bank-Account-Verification-FAQ)is an additional step in the onboarding process for Currencycloud BV clients. Completing the verification process triggers a push notification.

## Versions

1. [Version 2021-02-01](#version-2021-02-01)  
2. [Version 2021-01-01](#version-2021-01-01)

## Version 2021 02 01

We have updated the header content-type to JSON in this version. All other details remain the same.

#### Notification Type: **Ready To Send Notification**
#### Message Header

```
Content-Length: 681
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_ready_to_send_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "ready_to_send",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Released Notification**
#### Message Header
```
Content-Length: 734
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_released_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "completed",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Failed Notification**

#### Message Header

```
Content-Length: 757
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_failed_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "failed",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "Test Fail",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Compliance Failed**

#### Message Header

```
Content-Length: 743
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_compliance_failed_notification"
  },
  "body": {
    "id": "ff13cd8a-d0b3-473c-a6e8-f68bc079aff8",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id":null,
    "currency": "GBP",
    "reference": "rrr",
    "reason": "test",
    "status": "failed",
    "payment_type": "priority",
    "payment_date": "2018-07-27T00:00:00+00:00",
    "transferred_at": null,
    "authorisation_steps_required": 0,
    "creator_contact_id": "eb5ecd81-f800-0132-a9c5-10b11cb33cfb",
    "last_updater_contact_id": "eb5ecd81-f800-0132-a9c5-10b11cb33cfb",
    "short_reference": "180727-GYJLVG001",
    "failure_reason": "Compliance failed 1",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```

---

#### Notification Type: **Cash Manager Trade Notification**

#### Message Header


```
Content-Length: 932
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{  

   "header":{  
      "message_type":"conversion",
      "notification_type":"cash_manager_trade_notification"
   },

   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"awaiting_funds",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"1.4078",
      "core_rate":"1.4077",
      "partner_rate":"",
      "client_rate":"1.3795",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }

}
```

---

#### Notification Type: **Funds Arrived Notification**

#### Message Header


```

Content-Length: 927
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"funds_arrived_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"funds_arrived",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":null,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```

---

#### Notification Type: **Trade Settled Notification**

#### Message Header


```
Content-Length: 922
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"trade_settled_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"trade_settled",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```
---

#### Notification Type: **Trade Closed Notification**

#### Message Header


```
Content-Length: 924
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"trade_closed_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"closed",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```

---

#### Notification Type: **Deposit Arrived Notification**

#### Message Header


```
Content-Length: 955
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
 "header":
 {
  "message_type":"conversion",
  "notification_type":"deposit_arrived_notification"
},

"body":
{
"id":"991e203b-5001-4cca-83f4-606e6543f6cd",
"account_id":"9658df0c-a7cd-d9c9-274a-4e81bdf5f64a",
"creator_contact_id":"a3180fae-4c77-6dfb-74b3-4f16d55d6d1d",
"short_reference":"20180514-TCNZVW",
"created_at":"2018-05-14T07:24:06+00:00",
"settlement_date":"2018-05-17T13:00:00+00:00",
"conversion_date":"2018-05-17T00:00:00+00:00",
"status":"awaiting_funds",
"currency_pair":"GBPUSD",
"buy_currency":"GBP",
"sell_currency":"USD",
"fixed_side":"buy",
"partner_buy_amount":"0.00",
"partner_sell_amount":"0.00",
"client_buy_amount":"1500.00",
"client_sell_amount":"2115.90",
"mid_market_rate":"0.7092",
"core_rate":"0.7092",
"partner_rate":"",
"client_rate":"0.7089",
"deposit_required":true,
"deposit_amount":"63.48",
"deposit_currency":"USD",
"deposit_status":"deposit_received",
"deposit_required_at":"2018-05-16T13:00:00+00:00",
"payment_ids":[]
}
}
```

---

#### Notification Type: **Transfer Created Notification**

#### Message Header

```

Content-Length: 612
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```

{  
   "header":{  
      "message_type":"transfer",
      "notification_type":"transfer_created_notification"
   },
   "body":{  
      "id":"c30f5835-2544-41d8-bf0c-4868669b637d",
      "short_reference":"BT-20180511-KZTTYX",
      "source_account_id":"e0bf0629-56e7-42f2-84a4-3528168ee21c",
      "destination_account_id":"10a1ba3d-10f8-400e-89fa-8fafa323cc96",
      "currency":"USD",
      "amount":"300.00",
      "status":"pending",
      "created_at":"2018-05-11T13:21:43+00:00",
      "updated_at":"2018-05-11T13:21:43+00:00",
      "completed_at":null,
      "creator_account_id":"2090939e-b2f7-3f2b-1363-4d235b3f58af",
      "creator_contact_id":"8a98ebac-6f88-e205-a685-4d235b1b088b",
      "reason":"moving funds 2 -> 3"
   }
}

```

---

#### Notification Type: **Transfer Completed Notification**

#### Message Header

```

Content-Length: 639
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```

      {  
   "header":{  
      "message_type":"transfer",
      "notification_type":"transfer_completed_notification"
   },
   "body":{  
      "id":"c30f5835-2544-41d8-bf0c-4868669b637d",
      "short_reference":"BT-20180511-KZTTYX",
      "source_account_id":"e0bf0629-56e7-42f2-84a4-3528168ee21c",
      "destination_account_id":"10a1ba3d-10f8-400e-89fa-8fafa323cc96",
      "currency":"USD",
      "amount":"300.00",
      "status":"completed",
      "created_at":"2018-05-11T13:21:43+00:00",
      "updated_at":"2018-05-11T13:21:44+00:00",
      "completed_at":"2018-05-11T13:21:44+00:00",
      "creator_account_id":"2090939e-b2f7-3f2b-1363-4d235b3f58af",
      "creator_contact_id":"8a98ebac-6f88-e205-a685-4d235b1b088b",
      "reason":"moving funds 2 -> 3"
   }
}

```

---

#### Notification Type: **Pending Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 723
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "pending_cash_manager_transaction_notification"
  },
  "body": {
    "id": "0c54e5d6-afd8-4eab-b82f-f2371467d79f",
    "balance_id": "b7a0b206-4dfd-48e6-aa7b-1b6514b76148",
    "account_id": "8427390b-21cc-41f5-b3b4-8ce20d770053",
    "currency": "EUR",
    "amount": "1000.00",
    "balance_amount": "1000.00",
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "46d8d68f-9fb1-41ba-9d67-708dc36d0cf1",
    "related_entity_short_reference": "IF-20200616-MMZ57O",
    "status": "pending",
    "reason": "",
    "settles_at": null,
    "created_at": "2020-06-16T12:13:47+00:00",
    "updated_at": "2020-06-16T12:13:47+00:00",
    "completed_at": null,
    "action": "funding"
  }
}

```

---

#### Notification Type: **Reject Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 742
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "reject_cash_manager_transaction_notification"
  },
  "body": {
    "id": "0c54e5d6-afd8-4eab-b82f-f2371467d79f",
    "balance_id": "b7a0b206-4dfd-48e6-aa7b-1b6514b76148",
    "account_id": "8427390b-21cc-41f5-b3b4-8ce20d770053",
    "currency": "EUR",
    "amount": "1000.00",
    "balance_amount": "1000.00",
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "46d8d68f-9fb1-41ba-9d67-708dc36d0cf1",
    "related_entity_short_reference": "IF-20200616-MMZ57O",
    "status": "deleted",
    "reason": "",
    "settles_at": null,
    "created_at": "2020-06-16T12:13:47+00:00",
    "updated_at": "2020-06-16T12:13:47+00:00",
    "completed_at": null,
    "action": "funding"
  }
}

```

---

#### Notification Type: **Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 711
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```

{
   "header":{
      "message_type":"cash_manager_transaction",
      "notification_type":"cash_manager_transaction_notification"
   },
   "body":{
      "id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "balance_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "account_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "currency":"EUR",
      "amount":"100000.00",
      "balance_amount":"100000.00",
      "type":"credit",
      "related_entity_type":"inbound_funds",
      "related_entity_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "related_entity_short_reference":"",
      "status":"completed",
      "reason":"",
      "settles_at":"2018-01-05T14:39:41+00:00",
      "created_at":"2018-01-05T14:39:41+00:00",
      "updated_at":"2018-01-05T14:39:41+00:00",
      "completed_at":"2018-01-05T14:39:41+00:00",
      "action":"funding"
   }
}

```
---

#### Notification Type: **End Client Application Received Notification**

#### Message Header

```
Content-Length: 280
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notifications

```
{
   "header":{
      "message_type":"onboarding",
      "notification_type":"end_client_application_received"
   },
   "body":{
      "submitted_at":"2022_04_12T10:15:48 00:00",
      "individual_applicant_name":"John Smith",
      "company_name":"ABC Ltd",
      "email":"john.smith@google.com",
      "form_id":"xyz123",
      "sub_account_id":"xyz123"
   }
}
```

---

#### Notification Type: **End Client Application Decisioned Notification**

#### Message Header

```
Content-Length: 369
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
   "header":{
      "message_type":"onboarding",
      "notification_type":"end_client_decisioned_webhook"
   },
   "body":{
      "entity_type":"Corporate",
      "individual_applicant_name":"John Smith",
      "company_name":"ABC Ltd",
      "trading_name":"ABC Ltd",
      "applicant_jurisdiction":"US",
      "contact_email":"john.smith@google.com",
      "contact_telephone":"07777777777",
      "Decision":"Approved",
      "sub_account_id":"xyz123",
      "sub_account_UUID":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   }

}
```

---

#### Notification Type: **Bank Account Verified Notification**

#### Message Header

```
Content-Length: 270
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: application/json
```

#### Push Notification

```
{
  "header": {
    "message_type": "bank_account_verified",
    "notification_type": "bank_account_verified_notification"
  },
  "body": {
    "account_id": "aae40a9f-6c91-3f2a-7678-4e92b3f83a6c",
    "account_name": "A New Account",
    "short_reference": "210401-48650",
    "bank_account_verified":"yes"
  }
```


## Version 2021 01 01

#### Notification Type: **Ready To Send Notification**
#### Message Header

```
Content-Length: 681
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_ready_to_send_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "ready_to_send",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Released Notification**
#### Message Header
```
Content-Length: 734
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_released_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "completed",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Failed Notification**

#### Message Header

```
Content-Length: 757
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_failed_notification"
  },
  "body": {
    "id": "a634d8c2-f520-4cba-985c-77dc1e0cc9af",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id": "e5e8c287-73c3-4998-a368-47937301e471",
    "currency": "GBP",
    "reference": "cc",
    "reason": "test",
    "status": "failed",
    "payment_type": "priority",
    "payment_date": "2018-04-30 00:00:00 +0000",
    "transferred_at": "2018-04-30 08:39:25 +0000",
    "authorisation_steps_required": "0",
    "creator_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "last_updater_contact_id": "202b6291-99b4-0132-60c0-10b11cb33cfb",
    "short_reference": "180430-TSLCQJ001",
    "failure_reason": "Test Fail",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```
---

#### Notification Type: **Payment Compliance Failed**

#### Message Header

```
Content-Length: 743
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
  "header": {
    "message_type": "payment",
    "notification_type": "payment_compliance_failed_notification"
  },
  "body": {
    "id": "ff13cd8a-d0b3-473c-a6e8-f68bc079aff8",
    "amount": "2000.00",
    "failure_returned_amount": "2000.00",
    "beneficiary_id": "509c6dd0-6b26-4fec-930f-937ddc428bba",
    "conversion_id":null,
    "currency": "GBP",
    "reference": "rrr",
    "reason": "test",
    "status": "failed",
    "payment_type": "priority",
    "payment_date": "2018-07-27T00:00:00+00:00",
    "transferred_at": null,
    "authorisation_steps_required": 0,
    "creator_contact_id": "eb5ecd81-f800-0132-a9c5-10b11cb33cfb",
    "last_updater_contact_id": "eb5ecd81-f800-0132-a9c5-10b11cb33cfb",
    "short_reference": "180727-GYJLVG001",
    "failure_reason": "Compliance failed 1",
    "payment_group_id":null,
    "unique_request_id":"Ciu4eNcYnq582hwK_8Cu47sk",
    "fee_amount": null,
    "fee_currency": null
  }
```

---

#### Notification Type: **Cash Manager Trade Notification**

#### Message Header


```
Content-Length: 932
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{  

   "header":{  
      "message_type":"conversion",
      "notification_type":"cash_manager_trade_notification"
   },

   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"awaiting_funds",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"1.4078",
      "core_rate":"1.4077",
      "partner_rate":"",
      "client_rate":"1.3795",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }

}
```

---

#### Notification Type: **Funds Arrived Notification**

#### Message Header


```

Content-Length: 927
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"funds_arrived_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"funds_arrived",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":null,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```

---

#### Notification Type: **Trade Settled Notification**

#### Message Header


```
Content-Length: 922
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"trade_settled_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"trade_settled",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```
---

#### Notification Type: **Trade Closed Notification**

#### Message Header


```
Content-Length: 924
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{  
   "header":{  
      "message_type":"conversion",
      "notification_type":"trade_closed_notification"
   },
   "body":{  
      "id":"a0d9034e-bc9f-45e7-a1e4-6485735794c0",
      "account_id":"d2b04c30-9585-4ba6-acea-bf9add10444d",
      "creator_contact_id":"669b4860-4bb3-4636-8ee4-9e672810d350",
      "short_reference":"20180430-GBMHXC",
      "created_at":"2018-04-30T12:49:06+00:00",
      "settlement_date":"2018-04-30T15:30:00+00:00",
      "conversion_date":"2018-04-30T00:00:00+00:00",
      "status":"closed",
      "currency_pair":"GBPUSD",
      "buy_currency":"USD",
      "sell_currency":"GBP",
      "fixed_side":"sell",
      "partner_buy_amount":"0.00",
      "partner_sell_amount":"0.00",
      "client_buy_amount":"96565.00",
      "client_sell_amount":"70000.00",
      "mid_market_rate":"0.7103",
      "core_rate":"0.7104",
      "partner_rate":"",
      "client_rate":"0.7249",
      "deposit_required":false,
      "deposit_amount":"0.00",
      "deposit_currency":"",
      "deposit_status":"not_required",
      "deposit_required_at":"",
      "payment_ids":[]
   }
}
```

---

#### Notification Type: **Deposit Arrived Notification**

#### Message Header


```
Content-Length: 955
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
 "header":
 {
  "message_type":"conversion",
  "notification_type":"deposit_arrived_notification"
},

"body":
{
"id":"991e203b-5001-4cca-83f4-606e6543f6cd",
"account_id":"9658df0c-a7cd-d9c9-274a-4e81bdf5f64a",
"creator_contact_id":"a3180fae-4c77-6dfb-74b3-4f16d55d6d1d",
"short_reference":"20180514-TCNZVW",
"created_at":"2018-05-14T07:24:06+00:00",
"settlement_date":"2018-05-17T13:00:00+00:00",
"conversion_date":"2018-05-17T00:00:00+00:00",
"status":"awaiting_funds",
"currency_pair":"GBPUSD",
"buy_currency":"GBP",
"sell_currency":"USD",
"fixed_side":"buy",
"partner_buy_amount":"0.00",
"partner_sell_amount":"0.00",
"client_buy_amount":"1500.00",
"client_sell_amount":"2115.90",
"mid_market_rate":"0.7092",
"core_rate":"0.7092",
"partner_rate":"",
"client_rate":"0.7089",
"deposit_required":true,
"deposit_amount":"63.48",
"deposit_currency":"USD",
"deposit_status":"deposit_received",
"deposit_required_at":"2018-05-16T13:00:00+00:00",
"payment_ids":[]
}
}
```

---

#### Notification Type: **Transfer Created Notification**

#### Message Header

```

Content-Length: 612
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```

{  
   "header":{  
      "message_type":"transfer",
      "notification_type":"transfer_created_notification"
   },
   "body":{  
      "id":"c30f5835-2544-41d8-bf0c-4868669b637d",
      "short_reference":"BT-20180511-KZTTYX",
      "source_account_id":"e0bf0629-56e7-42f2-84a4-3528168ee21c",
      "destination_account_id":"10a1ba3d-10f8-400e-89fa-8fafa323cc96",
      "currency":"USD",
      "amount":"300.00",
      "status":"pending",
      "created_at":"2018-05-11T13:21:43+00:00",
      "updated_at":"2018-05-11T13:21:43+00:00",
      "completed_at":null,
      "creator_account_id":"2090939e-b2f7-3f2b-1363-4d235b3f58af",
      "creator_contact_id":"8a98ebac-6f88-e205-a685-4d235b1b088b",
      "reason":"moving funds 2 -> 3"
   }
}

```

---

#### Notification Type: **Transfer Completed Notification**

#### Message Header

```

Content-Length: 639
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```

      {  
   "header":{  
      "message_type":"transfer",
      "notification_type":"transfer_completed_notification"
   },
   "body":{  
      "id":"c30f5835-2544-41d8-bf0c-4868669b637d",
      "short_reference":"BT-20180511-KZTTYX",
      "source_account_id":"e0bf0629-56e7-42f2-84a4-3528168ee21c",
      "destination_account_id":"10a1ba3d-10f8-400e-89fa-8fafa323cc96",
      "currency":"USD",
      "amount":"300.00",
      "status":"completed",
      "created_at":"2018-05-11T13:21:43+00:00",
      "updated_at":"2018-05-11T13:21:44+00:00",
      "completed_at":"2018-05-11T13:21:44+00:00",
      "creator_account_id":"2090939e-b2f7-3f2b-1363-4d235b3f58af",
      "creator_contact_id":"8a98ebac-6f88-e205-a685-4d235b1b088b",
      "reason":"moving funds 2 -> 3"
   }
}

```

---

#### Notification Type: **Pending Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 723
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "pending_cash_manager_transaction_notification"
  },
  "body": {
    "id": "0c54e5d6-afd8-4eab-b82f-f2371467d79f",
    "balance_id": "b7a0b206-4dfd-48e6-aa7b-1b6514b76148",
    "account_id": "8427390b-21cc-41f5-b3b4-8ce20d770053",
    "currency": "EUR",
    "amount": "1000.00",
    "balance_amount": "1000.00",
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "46d8d68f-9fb1-41ba-9d67-708dc36d0cf1",
    "related_entity_short_reference": "IF-20200616-MMZ57O",
    "status": "pending",
    "reason": "",
    "settles_at": null,
    "created_at": "2020-06-16T12:13:47+00:00",
    "updated_at": "2020-06-16T12:13:47+00:00",
    "completed_at": null,
    "action": "funding"
  }
}

```

---

#### Notification Type: **Reject Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 742
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "reject_cash_manager_transaction_notification"
  },
  "body": {
    "id": "0c54e5d6-afd8-4eab-b82f-f2371467d79f",
    "balance_id": "b7a0b206-4dfd-48e6-aa7b-1b6514b76148",
    "account_id": "8427390b-21cc-41f5-b3b4-8ce20d770053",
    "currency": "EUR",
    "amount": "1000.00",
    "balance_amount": "1000.00",
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "46d8d68f-9fb1-41ba-9d67-708dc36d0cf1",
    "related_entity_short_reference": "IF-20200616-MMZ57O",
    "status": "deleted",
    "reason": "",
    "settles_at": null,
    "created_at": "2020-06-16T12:13:47+00:00",
    "updated_at": "2020-06-16T12:13:47+00:00",
    "completed_at": null,
    "action": "funding"
  }
}

```

---

#### Notification Type: **Cash Manager Transaction Notification**

#### Message Header

```

Content-Length: 711
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```

{
   "header":{
      "message_type":"cash_manager_transaction",
      "notification_type":"cash_manager_transaction_notification"
   },
   "body":{
      "id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "balance_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "account_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "currency":"EUR",
      "amount":"100000.00",
      "balance_amount":"100000.00",
      "type":"credit",
      "related_entity_type":"inbound_funds",
      "related_entity_id":"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "related_entity_short_reference":"",
      "status":"completed",
      "reason":"",
      "settles_at":"2018-01-05T14:39:41+00:00",
      "created_at":"2018-01-05T14:39:41+00:00",
      "updated_at":"2018-01-05T14:39:41+00:00",
      "completed_at":"2018-01-05T14:39:41+00:00",
      "action":"funding"
   }
}

```
---

#### Notification Type: **End Client Application Submitted Notification**

#### Message Header

```
Content-Length: 280
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notifications

```
{
   "header":{
      "message_type":"end_client_application_submitted",
      "notification_type":"end_client_application_submitted_notification"
   },
   "body":{
      "submitted_at":"2024-10-11T11:21:21.000Z",
      "individual_applicant_name":null,
      "company_name":"Company Name Ltd",
      "email":"firstname.lastname@company.com",
      "form_id":"a12b123ce-1ab2-123c-a21b-12a12b123c12",
      "sub_account_id":"c23d234df-2bc3-234d-b32c-23b23c234d23"
   }
}
```
---

#### Notification Type: **End Client Application Decisioned Notification**

#### Message Header

```
Content-Length: 369
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
 "header": {
  "message_type": "end_client_application_decisioned",
  "notification_type": "end_client_application_decisioned_notification"
 },
 "body": {
  "entity_type": "corporate",
  "applicant_jurisdiction": "IE",
  "individual_applicant_name": null,
  "company_name": "Company Name Ltd",
  "trading_name": "",
  "contact_email": "firstname.lastname@company.com",
  "contact_telephone": "00353123123123",
  "decision": "approved",
  "form_id": "a12b123ce-1ab2-123c-a21b-12a12b123c12",
  "sub_account_id": "c23d234df-2bc3-234d-b32c-23b23c234d23"
 }
}
```
---

#### Notification Type: **Bank Account Verified Notification**

#### Message Header
```
Content-Length: 270
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: WS00CC014:8000
Content-Type: text/plain
```

#### Push Notification

```
{
  "header": {
    "message_type": "bank_account_verified",
    "notification_type": "bank_account_verified_notification"
  },
  "body": {
    "account_id": "aae40a9f-6c91-3f2a-7678-4e92b3f83a6c",
    "account_name": "A New Account",
    "short_reference": "210401-48650",
    "bank_account_verified":"yes"
  }
```
