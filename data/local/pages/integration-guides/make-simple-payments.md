[_metadata_:menu_title]:- "Making simple payments to beneficiaries"
[_metadata_:order]:- "5"

# Making simple payments to beneficiaries

## TL;DR

The steps and endpoints for making a simple payment are:

1. Check that you have enough balance in the payment currency - [Get Balance](/api-reference/#balances). Alternatively, [Find Balances](/api-reference/#find-balances) will tell you the value of all foreign currencies that you hold in your main Currencycloud account.
2.	Find an existing beneficiary or create a new one - [Find Beneficiaries](/api-reference/#find-beneficiaries) / [Create Beneficiary](/api-reference/#create-beneficiary).
3.	Find out what payer details are required for the payment - [Get Payer Requirements](/api-reference/#get-payer-requirements).
4.	Create the payment - [Create Payment](/api-reference/#create-payment).

Detailed instructions are given below.

## Workflow diagrams

### House accounts

#### Beneficiaries and payments (when creating a new beneficiary)
![beneficiaries and payments](/images/workflow_diagrams/8_beneficiaries_and_payments_new_beneficiary.jpg)

#### Beneficiaries and payments
##### when using a beneficiary that already exists
![beneficiaries and payments](/images/workflow_diagrams/9_beneficiaries_and_payments_existing_beneficiary.jpg)  

### Sub-accounts (on behalf of)

#### Beneficiaries and payments - on behalf of (when creating a new beneficiary)
![beneficiaries and payments](/images/workflow_diagrams/6_beneficiaries_and_payments_on_behalf_of_new_beneficiary.jpg)

#### Beneficiaries and payments - on behalf of (when using a beneficiary that already exists)
![beneficiaries and payments](/images/workflow_diagrams/7_beneficiaries_and_payments_on_behalf_of_existing_beneficiary.jpg)


## Integration guide

A payment is a transfer of money from a payer's account to a beneficiary.

Payments cannot be made in one currency and received in another. To pay a beneficiary in a particular currency, the payer must hold funds in that currency. If necessary, the payer must convert funds from one currency to another before making a payment.

In this guide, you will:

-   Check how much money you hold in various foreign currencies.
-   Use funds from your Euros balance to make a payment in Euros to a beneficiary in Germany.

## Step 1: Login

Please refer to the [Authentication guide](/guides/integration-guides/authentication) for instructions for starting a new API session.

## Step 2: Check available balances

To find out how many Euros you have, call the [Get Balance](/api-reference/#get-balance) endpoint, passing `EUR` as the third URI path parameter.

```
GET /v2/balances/EUR
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

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

```
GET /v2/balances/find
X-Auth-Token: ea6d13c7bc50feb46cf978d137bc01a2

```

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

## Step 3: Check payment requirements

Currencycloud supports two types of payments:

-   **Regular (local) payments**: Made using the local bank network. Regular payments are normally received by beneficiaries within five working days of the settlement date. This is a good choice for low-value, non-urgent transactions.
-   **Priority (Swift) payments**: Made using the Swift network. Payments can be made to over 212 countries, and 95% of payments arrive within one working day.

As an example, consider the situation where you need to make regular (local) payments to a supplier based in Germany. You have enough funds in your Euros balance to make the payment, there is therefore no need to top-up your Euros balance beforehand.

First, check what details are required to make a regular (local) payment in Euros to a beneficiary with a bank account in Germany. To do that, call the [Get Beneficiary Requirements](/api-reference/#get-beneficiary-requirements) endpoint.

`GET /v2/reference/beneficiary_required_details`

| Parameter Name | Parameter Type | Example Value |
| --- | --- | --- |
| `currency` | Query String | `EUR` |
| `bank_account_country` | Query String | `DE` |
| `X-Auth-Token` | Header | `ea6d13c7bc50feb46cf978d137bc01a2` |

The following response tells us that, to make a regular payment to a German bank account in Euros, we need two pieces of information: the IBAN and BIC/Swift numbers for the beneficiary. The beneficiary could be either a company or an individual. Either way, the same information is required.

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

## Step 4: Add a beneficiary

If you are a client under the Sponsored or Treasury service model and contracted with The Currency Cloud Limited, then you must [verify the beneficiary's account](/guides/integration-guides/verifying-beneficiary-account) details before creating a beneficiary.

If you know the required details, you can go ahead and create a record for the beneficiary via the [Create Beneficiary](/api-reference/#create-beneficiary) endpoint.

`POST /v2/beneficiaries/create`\
`Content-Type: multipart/form-data`


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

## Step 5: Make a payment

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

If the payment is successfully queued, the response payload will contain all the information about the payment as recorded in your Currencycloud account. This does not mean that the payment has been made, it just means that it is ready for processing.

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

Payments are processed first-in, first-out. Currencycloud will process payments on the `payment_date` specified, provided you hold enough money in the relevant currency at the time.

Once the payment is released, the beneficiary is cloned and the cloned version becomes read-only. Find out more in our [Preserving Beneficiaries Details](/guides/platform-specifics/preserving-beneficiary-details) article.
