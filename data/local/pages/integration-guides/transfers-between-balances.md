[_metadata_:menu_title]:- "Transferring funds between balances"
[_metadata_:order]:- "5"

# Transferring funds between balances

Transfers allow you to manage the movement of funds between the balances of your Currencycloud accounts. You can move funds from your house account to sub-accounts, sub-account to sub-account, and sub-account to house account.

In this integration guide, we will cover how to transfer balance from one account to another. Please note that no currency conversion is performed during a transfer, the sending and receiving accounts must therefore hold money in the same currency.

## Step 1: Login

Please refer to the [Authentication guide](/guides/integration-guides/authentication) for instructions to start a new API session.

## Step 2: Check balance

In the [Checking you balances guide](/guides/integration-guides/checking-your-balances), we covered how to find out the account balance for a specific currency as well as how to obtain an account balance for each currency you have available.

Before proceeding with a transfer it is worth checking the balances you have available. If there are insufficient funds available on the balance to complete the transfer, the transfer transaction will remain in a 'pending' status until sufficient funds are available.

## Step 3: Instruct the transfer

The [Create Transfer](/api-reference/#create-transfer) endpoint allows you to transfer a currency balance from a source account to a destination account.


`POST /v2/transfers/create`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `currency` | Form Data | `EUR` |
| `source_account_id` | Form Data | `aea097c2-39e4-49b5-aaa6-c860ca55ca0b` |
| `destination_account_id` | Form Data | `22ed17b5-b90c-424e-aa78-d24928b1778e` |
| `reason` | Form Data | `funds movement` |
| `amount` |  Form Data | 1000.00 |
| `X-Auth-Token` |  Header |  `ea6d13c7bc50feb46cf978d137bc01a2` |

```

{
  {
    "id": "883c665f-c8ee-475a-98f1-b88d73bfbf3e",
    "short_reference": "BT-20190301-FFSXLC",
    "source_account_id": "cf28b2d8-5afa-4d7f-9a26-7b45bf616a11",
    "destination_account_id": "22ed17b5-b90c-424e-aa78-d24928b1778e",
    "currency": "GBP",
    "amount": "100.00",
    "status": "pending",
    "reason": null,
    "created_at": "2019-03-01T16:44:30+00:00",
    "updated_at": "2019-03-01T16:44:30+00:00",
    "completed_at": null,
    "creator_account_id": "72970a7c-7921-431c-b95f-3438724ba16f",
    "creator_contact_id": "a66ca63f-e668-47af-8bb9-74363240d781"
  }
}
```

## Step 4: Push notifications

You can ingest transfer push notifications, please refer to our [push notifications guide](/guides/docs/getting-started/push-notifications) for more details.

## Step 5: Confirm transfer completed

You can either call the [Get Balance](/api-reference/#get-balance) endpoint to confirm that the account has been updated with the correct amount of funds or use the Find Transaction [Find Transactions](/api-reference/#find-transactions) endpoint with an action of 'transfer' to confirm that the instruction has taken place.
