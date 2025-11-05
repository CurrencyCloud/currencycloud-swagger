[_metadata_:menu_title]:- "Inbound Funds / Collections"
[_metadata_:order]:- "9"

# Inbound Funds / Collections

This guide demonstrates how to use push notifications and API calls to reconcile funds received into a Currencycloud account.

## TL;DR
1.  To receive funds into a Currencycloud account, you need to know the account details. These can be obtained by making a request to the [Find Funding Accounts](/api-reference/#funding) endpoint.
2.  Once funds have been settled to a Currencycloud account, you can ingest funding push notifications to be notified that funds have arrived. This messaging can be customized and displayed within your application. Please refer to our [push notifications page](/guides/getting-started/push-notifications) for more details. 
3.  To see the transaction details, call the [Find Transactions](/api-reference/#find-transactions) endpoint.
4.  The [Get Sender Details](/api-reference/#get-sender-details) endpoint gives you more information about the sender and the payment rail.
5.  The [Accept or Reject Inbound Transaction](/api-reference/#transaction-approval) endpoint gives you the ability to screen an inbound transaction if you have opted in to the service.   


Detailed instructions are given in the integration guide below.

## Workflow diagram

![collections](/images/workflow_diagrams/2_find_funding_account_collections-and-settlements.jpg)


## Integration guide
This guide assumes that your customers provide settlement details to their customers and where you are supporting sub-accounts. For more information on sub-account activity, please reference our [sub-account activity guide.](/guides/integration-guides/sub-account-activity)

## Step 1: Login  

Please refer to the [authentication guide](/guides/integration-guides/authentication) for instructions on how to start a new API session.

## Step 2: Locate funding/SSI details  

Find the necessary settlement account details for the specific currency your customer will want to receive funds in by calling the [Find Funding Accounts](/api-reference/#find-funding-accounts) endpoint. 

In the example below, we are locating the account details used for collecting/funding Euros by passing in `payment_type` as 'regular', `currency` as 'EUR',  and the appropriate customer `account-id` (sub-account id) as query parameters. 

**Request:**

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |
| `payment_type` | Query String | `regular` |
| `currency` | Query String | `EUR` |
| `account_id` | Query String | `156d8d0e-2f05-4ffc-b7da-2b0be576bbb0` |

**Response:**

```

{
   "funding_accounts": [
     {
        "id": "9159cd45-ee3d-4e58-b2d7-00c5a68600c1",
        "account_id": "156d8d0e-2f05-4ffc-b7da-2b0be576bbb0",
        "account_number":"GB01TCCL06642902435207",
        "account_number_type": "iban",
        "account_holder_name": "Jimmy's Burritos_store 1",
        "bank_name": "The Currency Cloud Limited",
        "bank_address": "12 Steward Street, The Steward Building, London, E1 6FQ, GB",
        "bank_country": "GB",
        "currency": "EUR",
        "payment_type": "regular",
        "routing_code": "TCCLGB31",
        "routing_code_type": "bic_swift",
        "created_at": "2021-02-02T15:22:22+00:00",
        "updated_at": "2021-02-02T15:22:22+00:00"
     }
   ],
  "pagination": {
        "total_entries": 1,
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

Based on the above response, we can use the necessary IBAN and bank information to appropriately fund Euros into the respective Currencycloud Account. Since the `payment_type parameter` is set to 'regular', an individual or company that is sending funds into the account will be able to use the local SEPA network using a local bank account that is domiciled somewhere in the EEA region.

Keep in mind that these settlement instructions can be used by your customer, or your customer can send these details directly onto one of their customers (aka 4th party), depending on the account structure/compliance model that you have with Currencycloud.

## Step 3: Consume push notifications


Once funds have been settled to a Currencycloud account, you can ingest funding push notifications indicating that funds have arrived. This messaging can be customized and displayed within your application. Please refer to our [push notifications page](/guides/getting-started/push-notifications) for more details. 

### **Funding transaction**

The following diagram presents the details of a funding transaction.

![](/images/push_notifications/pn_funding_transactions_diagram.png)

Below are examples of both a "pending" and "completed" status push notification described in the diagram above, using  our current example of funding Euros to an account.


**Message Header**  


```
Content-Length: 675
Accept-Encoding: gzip;q=1.0,deflate;q=0.6,identity;q=0.3
Accept: */*
User-Agent: Ruby
Host: webhook.site
x-hmac-digest-sha-512 e7ace9c29306a82b25bdb764f60f583aeb9145e17c06572640a2953c243e97e19dde7e5cf00b10e60e5ede255b5c91c09312dbec58b7f695d9801fa90514a1dd
Content-Type: text/plain
```

**Notification Type:** Pending Cash Manager Transaction Notification

**Push Notification:**  


```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "pending_cash_manager_transaction_notification"
  },
  "body": {
    "id": "1b5d9096-74ef-4988-9d12-62662ee0e2a8",
    "balance_id": "2e6056ce-660f-4b4c-9470-27d8706f08ed",
    "account_id": "156d8d0e-2f05-4ffc-b7da-2b0be576bbb0",
    "currency": "EUR",
    "amount": "1000.00",
    "balance_amount": null,
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "1f453dcb-05c3-4320-806f-2c86d0fe6ed2",
    "related_entity_short_reference": "IF-20210409-VMN9TQ",
    "status": "pending",
    "reason": "",
    "settles_at": null,
    "created_at": "2021-04-09T16:57:55+00:00",
    "updated_at": "2021-04-09T16:57:55+00:00",
    "completed_at": null,
    "action": "funding"
  }
}

```

**Notification Type:** Cash Manager Transaction Notification  

**Push Notification:**  


```

{
  "header": {
    "message_type": "cash_manager_transaction",
    "notification_type": "cash_manager_transaction_notification"
  },
  "body": {
    "id": "1b5d9096-74ef-4988-9d12-62662ee0e2a8",
    "balance_id": "2e6056ce-660f-4b4c-9470-27d8706f08ed",
    "account_id": "156d8d0e-2f05-4ffc-b7da-2b0be576bbb0",
    "currency": "EUR",
    "amount": "10000.00",
    "balance_amount": "1000010000.00",
    "type": "credit",
    "related_entity_type": "inbound_funds",
    "related_entity_id": "1f453dcb-05c3-4320-806f-2c86d0fe6ed2",
    "related_entity_short_reference": "IF-20210409-VMN9TQ",
    "status": "completed",
    "reason": "",
    "settles_at": "2021-04-09T16:57:58+00:00",
    "created_at": "2021-04-09T16:57:55+00:00",
    "updated_at": "2021-04-09T16:57:58+00:00",
    "completed_at": "2021-04-09T16:57:58+00:00",
    "action": "funding"
  }
}

```


## Step 4 (optional): Retrieve transaction details


From a reporting perspective, you can pull down transaction activity both at the house account or sub-account level. If we want to locate the funding transaction from the above received push notification we can call the [Find Transactions](/api-reference/#find-transactions) endpoint.

In the example below, we are using the `currency`, `amount`, and `related_entity_id` (parsed from the above push notification), as query parameters.

**Request:**  


| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |
| `currency` | Query String | `EUR` |
| `amount` | Query String | `10000.00` |
| `related_entity_id` | Query String | `1f453dcb-05c3-4320-806f-2c86d0fe6ed2` |

**Response**:  


```
{
  "transactions": [
     {
         "id": "1b5d9096-74ef-4988-9d12-62662ee0e2a8",
         "balance_id": "2e6056ce-660f-4b4c-9470-27d8706f08ed",
         "account_id": "156d8d0e-2f05-4ffc-b7da-2b0be576bbb0",
         "currency": "EUR",
         "amount": "10000.00",
         "balance_amount": "1000010000.00",
         "type": "credit",
         "related_entity_type": "inbound_funds",
         "related_entity_id": "1f453dcb-05c3-4320-806f-2c86d0fe6ed2",
         "related_entity_short_reference": "IF-20210409-VMN9TQ",
         "status": "completed",
         "reason": "",
         "settles_at": "2021-04-09T16:57:58+00:00",
         "created_at": "2021-04-09T16:57:55+00:00",
         "updated_at": "2021-04-09T16:57:58+00:00",
         "completed_at": "2021-04-09T16:57:58+00:00",
         "action": "funding"
    }
   ],
  "pagination": {
        "total_entries": 1,
        "total_pages": 1,
        "current_page": 1,
        "per_page": 25,
        "previous_page": -1,
        "next_page": -1,
        "order": "default",
       "order_asc_desc": "asc"
  }
}
```

## Step 5 (optional): Retrieve sender details

The [Sender API](/api-reference/#get-sender-details) gives you more visibility on inbound payments, allowing you to reconcile funds no matter the payment rail. In combination with our push notifications, users have a powerful tool for automated real time reconciliation. Below is an example using the UUID parsed from step 3 as a URI path.

**Request:**  

| **Parameter Name** | **Parameter Type** | **Example Value** |
| --- | --- | --- |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |
| `id` | Path | `1f453dcb-05c3-4320-806f-2c86d0fe6ed2` |

**Response**:   

```

{
  "id": "1f453dcb-05c3-4320-806f-2c86d0fe6ed2",
    "amount": "12000.00",
    "currency": "EUR",
    "additional_information": "Payment to CC",
    "value_date": "2021-05-25T00:00:00+00:00",
    "sender": "John Smith;100 Bishopsgate, London, EC2M 1GT;GB;GB29NWBK60161331926819;NWBKGB2L;"
    "receiving_account_number": null,
    "receiving_account_iban": "GB41TCCL04140419897139",
    "created_at": "2021-05-25T06:38:09+00:00",
    "updated_at": "2021-05-25T06:38:13+00:00"
}

```

Further explanation for some of the information that can be obtained from the above response is given below.

| Field | Explanation |
| --- | --- |
| `additional_information` | The payment reference provided by the sender and sending bank. |
| `sender` | The sending IBAN, BIC, Name and Address presented in the format   "sender":"{sender.name};{sender.address};{sender.country};{sender.account_number} or {sender.iban};{sender.bic};{sender.routing_code}"  Not all of these fields will be provided depending on the data received from the sending bank.|
| `receiving_account_number` | The virtual bank account details the payment was made to. In the above example, an IBAN was used instead of an account number. The response will show as "null" in this case.  |
| `receiving_account_iban` | The virtual account the payment was made to. In the above example, funds were sent to account:  GB41TCCL04140419897139 |

## Step 6 (optional): Accept or reject inbound transaction

This is an opt-in service that allows you to review and decide on inbound transactions. It applies to the payment rails listed below:

| Currency | Rail |
| --- | --- |
| EUR | SEPA |
| USD | ACH |
| CAD | EFT |
| GBP | FPS |

 You have 23.5 hours to respond from when the “pending cash manager transaction notification” is triggered (‘pending’ status).  If no response is received in this time, the default action is to accept the transaction. The transaction will then undergo our internal screening.  

 Both your decision and our internal screening result are required before the transaction is processed. If both parties approve, the funds are processed and the “cash manager transaction notification” is triggered when the funds are credited to the beneficiary's account (‘completed’ status). If either party rejects the transaction, the funds are automatically returned to the original sender for the payment rails specified above. For other payment rails, the funds should be manually returned. In the case of a rejection, the “rejected cash manager transaction notification” is triggered (‘deleted’ status).


### Push notifications

The result of compliance checks made by Currencycloud and you determine whether the transaction is processed or not and which push notification is triggered.

![push notifications screening](/images/push_notifications/pn_funding_transactions_with_screening.png)

### Workflow diagram

You should notify us of the result of your screening using the Accept or Reject Inbound Transaction endpoint.

![workflow diagram screening](/images/workflow_diagrams/12_funding_account_collections_with_screening.jpg)

### Endpoint Reference Information

*Name:* Accept or Reject Inbound Transaction

*Path:*  `/collections_screening/{transaction_id}/complete`

**Request:**  

| **Parameter Name** | **Parameter Location** | **Parameter Type** | **Description** |
| --- | --- | --- | --- |
| X-Auth-Token * | Header | string | Authentication Token |
| transaction_id *| Path | string | Transaction UUID |
| accepted *| formData | boolean | Should the transaction be accepted? true or false |
| reason *| formData | string | Reason for acceptance / rejection <br> Valid Acceptance options:<br> - Accepted <br><br> Rejection reasons: <br> - Sanctioned Match <br> - Unsupported Currency <br> - Insufficient Trnasaction Information <br> - Suspected Fraud <br> - Internal Watchlist Match <br> - Suspected Money Laundering Activity |

\* Required field

**Example Success Response:**

```
{
    "transaction_id": "a35c9c49-fb52-466d-9172-afbde1532c82",
    "account_id": "7a116d7d-6310-40ae-8d54-0ffbe41dc1c9",
    "house_account_id": "7a116d7d-6310-40ae-8d54-0ffbe41dc1c9",
    "result": {
        "reason": "Accepted",
        "accepted": true
    }
}
```

**Response Fields**

| **Name** | **Type** | **Description** |
| --- | --- | --- |
|transaction_id|string|Transaction UUID|
|account_id|string|House account or sub-account UUID|
|house_account_id|string|House account UUID|
|reason|string|Reason for acceptance / rejection|
|accepted|boolean|Accepted -- true or false.|
